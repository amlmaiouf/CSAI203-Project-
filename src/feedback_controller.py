from flask import Blueprint, request, redirect, url_for, render_template
from models.feedback_model import Feedback
from core.db_singleton import Database

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")


@feedback_bp.route("/", methods=["GET"])
def feedback_page():
    return render_template("Feedback.html")


@feedback_bp.route("/submit", methods=["POST"])
def submit_feedback():

    feedback = Feedback(
        service_name=request.form["serviceName"],
        rating=request.form["rating"],
        user_name=request.form["userName"],
        comment=request.form["comment"])

    db = Database()
    cursor = db.get_cursor()

    cursor.execute("""
        INSERT INTO feedbacks (service_name, rating, user_name, comment)
        VALUES (%s, %s, %s, %s)
    """, (
        feedback.service_name,
        feedback.rating,
        feedback.user_name,
        feedback.comment))

    db.commit()

    return redirect(url_for("feedback.feedback_page"))