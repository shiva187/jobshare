from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this in real deployment

# Initialize DB
def init_db():
    if not os.path.exists("jobs.db"):
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
        c.execute('''CREATE TABLE jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        company TEXT,
                        role TEXT,
                        link TEXT,
                        posted_by TEXT,
                        status TEXT DEFAULT 'Open')''')
        # Default user
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
        conn.commit()
        conn.close()

init_db()

# Database helper
def query_db(query, params=(), fetch=False):
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute(query, params)
    data = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data

# Home page (list jobs)
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
        query_db("INSERT INTO jobs (title, company, role, link, posted_by) VALUES (?, ?, ?, ?, ?)",
                 (title, company, role, link, posted_by))
        return redirect(url_for("index"))
    return render_template("add_job.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = query_db("SELECT * FROM users WHERE username=? AND password=?", (username, password), fetch=True)
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
    app.run(debug=True)
