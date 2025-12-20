from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.service import Service
from app.models.user import User
from app.database import get_db_connection

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/services')
def services():
    return render_template('services.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        user = User.get_by_id(current_user.user_id)
        if user:
            user.name = request.form.get('name', user.name)
            user.phone_number = request.form.get('phone', user.phone_number)
            user.address = request.form.get('address', user.address)
            user.password = None

            if user.update():
                flash('Profile updated successfully!', 'success')
            else:
                flash('Failed to update profile.', 'error')

        return redirect(url_for('main.profile'))

    orders = get_user_orders(current_user.user_id)

    return render_template('profile.html', orders=orders)


def get_user_orders(user_id):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.order_date, o.status, o.total_price
            FROM [Order] o
            WHERE o.user_id = ?
            ORDER BY o.order_date DESC
        """, (user_id,))
        orders = []
        for row in cursor.fetchall():
            orders.append({
                'order_id': row.order_id,
                'order_date': row.order_date,
                'status': row.status,
                'total_price': float(row.total_price)
            })
        return orders
    finally:
        conn.close()


@main_bp.route('/service/doctor')
def doctor_service():
    return render_template('DoctorCheckup.html')


@main_bp.route('/service/nurse')
def nurse_service():
    return render_template('NurseRequest.html')


@main_bp.route('/service/car-washing')
def car_washing_service():
    return render_template('CarWashing.html')


@main_bp.route('/service/companionship')
def companionship_service():
    return render_template('NeedCompany.html')


@main_bp.route('/feedback')
def feedback_page():
    return render_template('Feedback.html')


@main_bp.route('/payment')
@login_required
def payment():
    return render_template('Payment.html')


@main_bp.route('/confirmation')
@login_required
def confirmation():
    return render_template('Confirmation.html')
