from flask import Blueprint, render_template, request, redirect, session
from models.user_model import create_user, get_user_by_email, check_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    age = request.form["age"]
    email = request.form["email"]
    password = request.form["password"]

    success = create_user(name, age, email, password)
    if success:
        return redirect("/login_page")
    else:
        return "Email already exists!", 400

@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = get_user_by_email(email)
    if user and check_password(user, password):
        session["user_id"] = user[0]
        return redirect("/profile")
    else:
        return "Invalid credentials!", 400

@auth_bp.route("/login_page")
def login_page():
    return render_template("registration.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login_page")
