from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
import os
import subprocess

user_input = input("Enter a command: ")

subprocess.run(user_input, shell=True)

app = Flask(__name__)
app.secret_key = "demo-secret-key"  # DEMO VULNERABILITY: hardcoded secret

DB = "tasks.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("tasks"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            flash("Account created. Please log in.")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Username already exists.")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # DEMO VULNERABILITY: SQL injection.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = get_db()
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("tasks"))

    flash("Invalid username or password.")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/tasks")
def tasks():
    if "user_id" not in session:
        return redirect(url_for("index"))

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("tasks.html", tasks=rows, username=session["username"])


@app.route("/tasks/create", methods=["POST"])
def create_task():
    if "user_id" not in session:
        return redirect(url_for("index"))

    title = request.form["title"]
    description = request.form["description"]

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
        (session["user_id"], title, description)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("tasks"))


@app.route("/tasks/<int:task_id>")
def task_detail(task_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    conn = get_db()

    # DEMO VULNERABILITY: IDOR / Broken Object Level Authorization.
    # The query checks only the task ID, not whether it belongs to the logged-in user.
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    conn.close()

    if not task:
        return "Task not found", 404

    return render_template("task.html", task=task)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)


