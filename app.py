from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users.db")


@app.route("/")
def home():
    return render_template("index.html")


# REGISTER (CREATE)
@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()

    conn.execute(
        "INSERT INTO users (username,password) VALUES (?,?)",
        (username,password)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# LOGIN
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()

    cur = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user = cur.fetchone()

    conn.close()

    if user:
        return f"Welcome {username}!"
    else:
        return "Invalid Username or Password"


# READ USERS
@app.route("/users")
def users():

    conn = get_db()

    cur = conn.execute("SELECT id,username FROM users")

    data = cur.fetchall()

    conn.close()

    return str(data)


# UPDATE USER
@app.route("/update", methods=["POST"])
def update():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()

    conn.execute(
        "UPDATE users SET password=? WHERE username=?",
        (password,username)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# DELETE USER
@app.route("/delete", methods=["POST"])
def delete():

    username = request.form["username"]

    conn = get_db()

    conn.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    conn = sqlite3.connect("users.db")

    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )

    conn.close()

    app.run(host="0.0.0.0", port=5000)