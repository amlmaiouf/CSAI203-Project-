from flask import Blueprint, render_template, request, redirect, url_for, flash
from Models.payment_model import Payment

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")

@payment_bp.route("/", methods=["GET", "POST"])
def make_payment():
    if request.method == "POST":
        service_name = request.form.get("serviceName")
        full_name = request.form.get("fullName")
        phone = request.form.get("phone")
        payment_method = request.form.get("paymentMethod")
        card_number = request.form.get("cardNumber")
        expiry_date = request.form.get("expiryDate")
        cvv = request.form.get("cvv")
        vodafone_number = request.form.get("vodafoneNumber")

        payment = Payment(
            service_name=service_name,
            full_name=full_name,
            phone=phone,
            payment_method=payment_method,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            vodafone_number=vodafone_number
        )

        payment.save_to_csv()
        flash("Payment saved successfully!", "success")
        return redirect(url_for("payment.make_payment"))

    return render_template("payment.html")
