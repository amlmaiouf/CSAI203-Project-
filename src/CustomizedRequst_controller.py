from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db_connection
from models.CustomizedRequst_model import CustomizedRequest

custom_bp = Blueprint("customized", __name__, url_prefix="/customized")

# Show form page
@custom_bp.route("/")
def form():
    return render_template("Customized_Request.html")

# Handle new request submission
@custom_bp.route("/new", methods=["POST"])
def new_request():
    cr = CustomizedRequest(
        service_name=request.form.get("serviceName", "Customized Request"),
        name=request.form["fullName"],
        phone=request.form["phone"],
        email=request.form["email"],
        address=request.form["address"],
        date=request.form.get("date"),
        request=request.form["request"],
        notes=request.form.get("notes"),
        price=200  # set default price
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customized_requests
        (service_name, name, phone, email, address, date, request, notes, price)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cr.service_name,
        cr.name,
        cr.phone,
        cr.email,
        cr.address,
        cr.date,
        cr.request,
        cr.notes,
        cr.price
    ))

    request_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("customized.payment", request_id=request_id))

# Payment page
@custom_bp.route("/payment/<int:request_id>", methods=["GET", "POST"])
def payment(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customized_requests WHERE id = ?",
        (request_id,)
    )
    row = cursor.fetchone()

    order = None
    if row:
        columns = [column[0] for column in cursor.description]
        order = dict(zip(columns, row))

    cursor.close()
    conn.close()

    return render_template("Payment.html", order=order)

# Confirmation page
@custom_bp.route("/confirmation/", methods=["GET", "POST"])
def confirmation():
    return render_template("Confirmation.html")