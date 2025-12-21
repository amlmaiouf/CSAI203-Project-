from flask import Blueprint, render_template, redirect, session
from controllers.auth_controller import signup, login, logout

auth_bp = Blueprint("auth", __name__)

# =========================
# HOME (LOGIN / REGISTER)
# =========================
@auth_bp.route("/")
def home():
    return render_template("registration.html")


# =========================
# AUTH ROUTES
# =========================
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup_route():
    return signup()


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    return login()


@auth_bp.route("/logout")
def logout_route():
    return logout()


# =========================
# DASHBOARD (PROTECTED)
# =========================
@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    return render_template("dashboard.html")
