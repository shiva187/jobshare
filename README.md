# jobshare

**jobshare** is a simple Flask web application created to help users learn how to deploy projects online. This project demonstrates how to set up a basic web server, upload and share job listings, and use a cloud-hosted PostgreSQL database for persistent storage.

## Project Goals

- Build a basic Flask server with a web interface for job sharing.
- Learn how to deploy a Python project online (deployed on [Render.com](https://render.com/)).
- Use a PostgreSQL database (hosted on Render) so data persists even if the server goes inactive.
- Understand the difference between using a local database and a cloud database for persistence.

## Features

- **Add Jobs:** Submit job title, description, and link via an online form.
- **Persistent Storage:** All job data is stored in PostgreSQL, ensuring availability and reliability.
- **Deployment Practice:** Hands-on guide for deploying Flask apps and connecting to a managed database.

## Why Use PostgreSQL on Render?

- Cloud databases like PostgreSQL on Render keep your data even when the server goes inactive.
- Local databases lose any new data when the server restarts or goes offline.
- This project uses Render’s managed PostgreSQL to demonstrate robust data handling.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- psycopg2 or SQLAlchemy (for PostgreSQL integration)

### Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/shiva187/jobshare.git
    cd jobshare
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Database**
    - Set your PostgreSQL database URI from Render as an environment variable or in a `.env` file.

4. **Run the Application**
    ```bash
    flask run
    ```

### Deployment

- Deploy your app on [Render.com](https://render.com/) by connecting your GitHub repository.
- Create a PostgreSQL database from the Render dashboard and update your app’s configuration accordingly.

## Usage

- Access the web interface to add and view job postings.
- Data remains available thanks to the PostgreSQL backend.

## Technology Stack

- **Python** (Flask)
- **HTML/CSS**
- **PostgreSQL** (Database)
- **Render.com** (Deployment Platform)

## License

This project is for educational purposes. Feel free to use or modify it for your own learning.

---
