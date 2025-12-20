from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.database import get_db_connection
from app.models.order import Order
from app.models.user import User
from datetime import datetime


housekeeping_bp = Blueprint("housekeeping", __name__, url_prefix="/housekeeping")


@housekeeping_bp.route("/")
def housekeeping():
    """Display housekeeping request form."""
    return render_template("housekeeping.html")


@housekeeping_bp.route("/new", methods=["POST"])
def new_housekeeping():
    """Process new housekeeping request."""
    hk_type = request.form["Hktype"]
    notes = request.form.get("notes")
    name = request.form["fullName"]
    phone = request.form["phone"]
    email = request.form["email"]
    date = request.form["date"]
    price = 150

    # Determine user_id: use logged-in user or create/find guest user
    if current_user.is_authenticated:
        user_id = current_user.user_id
    else:
        user = User.get_by_email(email)
        if not user:
            user = User(
                name=name,
                email=email,
                password=None,
                role='Elderly',
                phone_number=phone
            )
            user.save()
        user_id = user.user_id

    # Create order
    order = Order(
        user_id=user_id,
        order_date=datetime.strptime(date, '%Y-%m-%d'),
        status='Pending',
        total_price=price,
        notes=f"Housekeeping: {hk_type}. {notes or ''}"
    )
    order.save()

    return redirect(url_for("housekeeping.payment", request_id=order.order_id))


@housekeeping_bp.route("/payment/<int:request_id>", methods=["GET", "POST"])
def payment(request_id):
    """Display payment page for housekeeping request."""
    order = Order.get_by_id(request_id)

    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('housekeeping.housekeeping'))

    # Get user details for phone number
    user = User.get_by_id(order.user_id)
    phone = user.phone_number if user else ''

    # Build dict for template compatibility
    order_dict = {
        'id': order.order_id,
        'type': 'Housekeeping',
        'name': order.customer_name,
        'phone': phone,
        'email': order.customer_email,
        'date': order.order_date,
        'price': order.total_price
    }

    return render_template("Payment.html", order=order_dict)


@housekeeping_bp.route("/confirmation/", methods=["GET", "POST"])
def confirmation():
    """Display confirmation page."""
    return render_template("Confirmation.html")
