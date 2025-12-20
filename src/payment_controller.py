from flask import Blueprint, request, redirect, url_for, render_template
from models.payment_model import Payment
from core.db_singleton import Database

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")

@payment_bp.route("/")
def payment_page():
    return render_template("Payment.html")


@payment_bp.route("/confirm", methods=["POST"])
def confirm_payment():

    payment = Payment(
        service_name=request.form["service_name"],
        name=request.form["name"],
        phone=request.form["phone"],
        email=request.form["email"],
        date=request.form["date"],
        price=request.form["price"],
        payment_method=request.form["payment_method"]
    )

    db = Database()
    cursor = db.get_cursor()

    cursor.execute("""
        INSERT INTO payments
        (service_name, name, phone, email, date, price, payment_method)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        payment.service_name,
        payment.name,
        payment.phone,
        payment.email,
        payment.date,
        payment.price,
        payment.payment_method
    ))

    db.commit()

    return redirect(url_for("payment.success"))