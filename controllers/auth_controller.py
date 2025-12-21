from flask import render_template, request, redirect, session, flash
from models.user import create_user, verify_user, init_db

init_db()

def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            create_user(username, email, password)
            return redirect("/login")
        except:
            flash("Username or email already exists")

    return render_template("signup.html")

def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = verify_user(username, password)
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")

        flash("Invalid credentials")

    return render_template("login.html")

def logout():
    session.clear()
    return redirect("/login")