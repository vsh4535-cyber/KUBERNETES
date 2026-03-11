from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users.db")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return f"Welcome {username}!"
    else:
        return "Invalid login"

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    conn.execute(
        "INSERT INTO users (username,password) VALUES (?,?)",
        (username, password)
    )
    conn.commit()
    conn.close()

    return "User registered successfully"


if __name__ == "__main__":
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.close()

    app.run(host="0.0.0.0", port=5000)