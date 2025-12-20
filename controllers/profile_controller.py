from flask import Blueprint, render_template, request, redirect, session
from models.user_model import get_user_by_id, update_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login_page")

    user = get_user_by_id(session["user_id"])

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        update_user(session["user_id"], name, age, email)
        user = get_user_by_id(session["user_id"])  # reload updated data

    return render_template("user_profile.html", name=user[1], age=user[2], email=user[3])
