from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

DB_NAME = "users.db"

# ---------- DATABASE SETUP ----------
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

init_db()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        form_type = request.form.get("form_type")  # login or register

        # ------------------ LOGIN ------------------
        if form_type == "login":
            email = request.form["signinEmail"]
            password = request.form["signinPassword"]

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
            conn.close()

            if user:
                session["user"] = {
                    "name": user[1],
                    "age": user[2],
                    "email": user[3]
                }
                return redirect(url_for("profile"))
            else:
                return "Invalid email or password"

        # ------------------ REGISTER ------------------
        elif form_type == "register":
            name = request.form["signupName"]
            age = request.form["signupAge"]
            email = request.form["signupEmail"]
            password = request.form["signupPassword"]

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO users (name, age, email, password) VALUES (?, ?, ?, ?)",
                    (name, age, email, password)
                )
                conn.commit()
                conn.close()
                return redirect(url_for("registration"))
            except sqlite3.IntegrityError:
                return "Email already exists"

    return render_template("registration.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("registration"))

    user = session["user"]
    return render_template("user_profile.html", name=user["name"], age=user["age"], email=user["email"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("registration"))

if __name__ == "__main__":
    app.run(debug=True)
