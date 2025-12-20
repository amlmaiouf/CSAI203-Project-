from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.payment_model import PaymentModel

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')
payment_model = PaymentModel()

@payment_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        service_name = request.form.get('serviceName')
        customer_name = request.form.get('fullName')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date = request.form.get('date')
        duration = request.form.get('duration')
        total_price = request.form.get('totalPrice')
        payment_method = request.form.get('paymentMethod')

        if not (service_name and customer_name and payment_method):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('order.payment'))

        payment_model.create_order(
            service_name, customer_name, phone, email, date,
            duration, total_price, payment_method
        )
        flash('Your payment has been processed successfully!', 'success')
        return redirect(url_for('order.payment'))

    return render_template('payment.html')
