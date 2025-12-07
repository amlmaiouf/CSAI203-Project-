from flask import render_template, request, redirect, url_for, session, flash
from models.user_model import create_user, get_user_by_email, verify_password

def show_registration():
    return render_template("registration.html")

def handle_auth():
    form_type = request.form.get("form_type")

    # ------- LOGIN -------
    if form_type == "login":
        email = request.form["signinEmail"]
        password = request.form["signinPassword"]

        user = get_user_by_email(email)

        if user and verify_password(user["password"], password):
            session["user"] = {
                "name": user["name"],
                "age": user["age"],
                "email": user["email"]
            }
            return redirect(url_for("profile_page"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("registration_page"))

    # ------- REGISTER -------
    elif form_type == "register":
        name = request.form["signupName"]
        age = request.form["signupAge"]
        email = request.form["signupEmail"]
        password = request.form["signupPassword"]

        if create_user(name, age, email, password):
            flash("Registration successful! Please log in.")
        else:
            flash("Email already exists!")

        return redirect(url_for("registration_page"))
