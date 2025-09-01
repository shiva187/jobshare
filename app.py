from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
app.secret_key = "supersecretkey" 

# PostgreSQL Connection
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d2qq8nadbo4c73cflmbg-a",
        user="jobsdb_0b0d_user",          # Change to your postgres user
        password="gmxH6nC6JgCtZsb6IWH5taQ4bEtPMUTY",         # Change to your postgres password
        database="jobsdb_0b0d"         # Make sure this DB exists in Postgres
    )
    return conn

# Initialize DB
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255))''')

    # Create jobs table
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    company VARCHAR(255),
                    role VARCHAR(255),
                    link TEXT,
                    posted_by VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'Open')''')

    # Insert default admin user if not exists
    c.execute("SELECT * FROM users WHERE username=%s", ("admin",))
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", "admin"))

    conn.commit()
    conn.close()

# Query helper
def query_db(query, params=(), fetch=False):
    conn = get_db_connection()
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute(query, params)
    data = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    jobs = query_db("SELECT * FROM jobs ORDER BY id DESC", fetch=True)
    return render_template("index.html", jobs=jobs, user=session["user"])

# Add job
@app.route("/add", methods=["GET", "POST"])
def add_job():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        company = request.form["company"]
        role = request.form["role"]
        link = request.form["link"]
        posted_by = session["user"]
        query_db("INSERT INTO jobs (title, company, role, link, posted_by) VALUES (%s, %s, %s, %s, %s)",
                 (title, company, role, link, posted_by))
        return redirect(url_for("index"))
    return render_template("add_job.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = query_db("SELECT * FROM users WHERE username=%s AND password=%s", 
                        (username, password), fetch=True)
        if user:
            session["user"] = username
            return redirect(url_for("index"))
        return "Invalid credentials! Try again."
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
