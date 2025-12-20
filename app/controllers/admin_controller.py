from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from functools import wraps
from app.models.user import User
from app.models.service import Service
from app.models.order import Order
from app.models.feedback import Feedback

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_services': Service.count_all(),
        'total_orders': Order.count_all(),
        'total_users': User.count_all(),
        'pending_orders': Order.count_by_status('Pending'),
        'total_feedback': Feedback.count_all(),
        'avg_rating': Feedback.get_average_rating(),
        'total_employees': len(User.get_employees()),
    }

    recent_orders = Order.get_recent(5)

    services = Service.get_all()
    top_services = []
    for svc in services[:5]:
        top_services.append({
            'service': svc,
            'request_count': svc.get_request_count(),
            'average_rating': svc.get_average_rating()
        })

    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         top_services=top_services)


@admin_bp.route('/services')
@login_required
@admin_required
def services_list():
    services = Service.get_all()

    for svc in services:
        svc.request_count = svc.get_request_count()
        svc.average_rating = svc.get_average_rating()
        svc.feedback_count = svc.get_feedback_count()

    return render_template('admin/services.html', services=services)


@admin_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    if request.method == 'POST':
        try:
            price = float(request.form.get('price', 0))
        except (ValueError, TypeError):
            price = 0

        service = Service(
            service_name=request.form.get('service_name'),
            type=request.form.get('type'),
            price=price,
            description=request.form.get('description'),
            is_available=request.form.get('is_available') == 'on'
        )

        if service.save():
            flash(f'Service "{service.service_name}" added successfully!', 'success')
            return redirect(url_for('admin.services_list'))
        else:
            flash('Failed to add service. Please try again.', 'error')

    return render_template('admin/service_form.html',
                         service=None,
                         service_types=Service.VALID_TYPES)


@admin_bp.route('/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(service_id):
    service = Service.get_by_id(service_id)

    if not service:
        flash('Service not found.', 'error')
        return redirect(url_for('admin.services_list'))

    if request.method == 'POST':
        try:
            price = float(request.form.get('price', 0))
        except (ValueError, TypeError):
            price = 0

        service.service_name = request.form.get('service_name')
        service.type = request.form.get('type')
        service.price = price
        service.description = request.form.get('description')
        service.is_available = request.form.get('is_available') == 'on'

        if service.update():
            flash(f'Service "{service.service_name}" updated successfully!', 'success')
            return redirect(url_for('admin.services_list'))
        else:
            flash('Failed to update service. Please try again.', 'error')

    return render_template('admin/service_form.html',
                         service=service,
                         service_types=Service.VALID_TYPES)


@admin_bp.route('/services/delete/<int:service_id>', methods=['POST'])
@login_required
@admin_required
def delete_service(service_id):
    service = Service.get_by_id(service_id)

    if not service:
        flash('Service not found.', 'error')
        return redirect(url_for('admin.services_list'))

    service_name = service.service_name

    if Service.delete(service_id):
        flash(f'Service "{service_name}" deleted successfully!', 'success')
    else:
        flash('Failed to delete service. It may have associated orders.', 'error')

    return redirect(url_for('admin.services_list'))


@admin_bp.route('/services/toggle/<int:service_id>', methods=['POST'])
@login_required
@admin_required
def toggle_service(service_id):
    service = Service.get_by_id(service_id)

    if not service:
        flash('Service not found.', 'error')
        return redirect(url_for('admin.services_list'))

    if Service.toggle_availability(service_id):
        status = 'disabled' if service.is_available else 'enabled'
        flash(f'Service "{service.service_name}" has been {status}.', 'success')
    else:
        flash('Failed to toggle service availability.', 'error')

    return redirect(url_for('admin.services_list'))


@admin_bp.route('/employees')
@login_required
@admin_required
def employees_list():
    employees = User.get_employees()
    return render_template('admin/employees.html', employees=employees)


@admin_bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_employee():
    if request.method == 'POST':
        if User.get_by_email(request.form.get('email')):
            flash('Email already registered.', 'error')
            return render_template('admin/employee_form.html', employee=None)

        employee = User(
            name=request.form.get('name'),
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password')),
            role=request.form.get('role'),
            phone_number=request.form.get('phone_number'),
            address=request.form.get('address')
        )

        if employee.save():
            flash(f'Employee "{employee.name}" added successfully!', 'success')
            return redirect(url_for('admin.employees_list'))
        else:
            flash('Failed to add employee. Please try again.', 'error')

    return render_template('admin/employee_form.html', employee=None)


@admin_bp.route('/employees/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_employee(user_id):
    employee = User.get_by_id(user_id)

    if not employee or employee.role not in ['Staff', 'Doctor', 'Caregiver']:
        flash('Employee not found.', 'error')
        return redirect(url_for('admin.employees_list'))

    if request.method == 'POST':
        employee.name = request.form.get('name')
        employee.email = request.form.get('email')
        employee.role = request.form.get('role')
        employee.phone_number = request.form.get('phone_number')
        employee.address = request.form.get('address')

        new_password = request.form.get('password')
        if new_password:
            employee.password = generate_password_hash(new_password)
        else:
            employee.password = None

        if employee.update():
            flash(f'Employee "{employee.name}" updated successfully!', 'success')
            return redirect(url_for('admin.employees_list'))
        else:
            flash('Failed to update employee. Please try again.', 'error')

    return render_template('admin/employee_form.html', employee=employee)


@admin_bp.route('/employees/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_employee(user_id):
    employee = User.get_by_id(user_id)

    if not employee or employee.role not in ['Staff', 'Doctor', 'Caregiver']:
        flash('Employee not found.', 'error')
        return redirect(url_for('admin.employees_list'))

    employee_name = employee.name

    if User.delete(user_id):
        flash(f'Employee "{employee_name}" deleted successfully!', 'success')
    else:
        flash('Failed to delete employee.', 'error')

    return redirect(url_for('admin.employees_list'))


@admin_bp.route('/performance')
@login_required
@admin_required
def service_performance():
    services = Service.get_all()

    performance_data = []
    for svc in services:
        request_count = svc.get_request_count()
        avg_rating = svc.get_average_rating()
        feedback_count = svc.get_feedback_count()
        revenue = svc.get_revenue()
        recent_feedback = svc.get_recent_feedback(3)

        performance_data.append({
            'service': svc,
            'request_count': request_count,
            'avg_rating': avg_rating,
            'feedback_count': feedback_count,
            'revenue': revenue,
            'recent_feedback': recent_feedback
        })

    performance_data.sort(key=lambda x: x['request_count'], reverse=True)

    total_requests = sum(p['request_count'] for p in performance_data)
    total_revenue = sum(p['revenue'] for p in performance_data)
    avg_rating = Feedback.get_average_rating()

    return render_template('admin/performance.html',
                         performance_data=performance_data,
                         total_requests=total_requests,
                         total_revenue=total_revenue,
                         avg_rating=avg_rating)


@admin_bp.route('/feedback')
@login_required
@admin_required
def feedback_list():
    service_id = request.args.get('service_id', type=int)
    rating = request.args.get('rating', type=int)

    if service_id or rating:
        feedback_items = Feedback.get_filtered(service_id=service_id, rating=rating)
    else:
        feedback_items = Feedback.get_all()

    services = Service.get_all()

    return render_template('admin/feedback.html',
                         feedback_items=feedback_items,
                         services=services,
                         selected_service=service_id,
                         selected_rating=rating)


@admin_bp.route('/feedback/delete/<int:feedback_id>', methods=['POST'])
@login_required
@admin_required
def delete_feedback(feedback_id):
    if Feedback.delete(feedback_id):
        flash('Feedback deleted successfully!', 'success')
    else:
        flash('Failed to delete feedback.', 'error')

    return redirect(url_for('admin.feedback_list'))
