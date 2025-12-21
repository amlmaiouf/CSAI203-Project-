import random
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from repositories.service_repository import ServiceRepository
from repositories.user_repository import UserRepository
from repositories.appointment_repository import AppointmentRepository

main_controller = Blueprint('main_controller', __name__)

# =========================================================
# 1. HOME & STATIC PAGES
# =========================================================

@main_controller.route('/')
@main_controller.route('/index.html')
def home():
    return render_template('index.html')

@main_controller.route('/about.html')
def about():
    return render_template('about.html')

@main_controller.route('/contact.html')
def contact():
    return render_template('contact.html')

# =========================================================
# 2. SERVICES (Read Operation)
# =========================================================

@main_controller.route('/services.html')
def services():
    # Fetch real data from DB via Repository
    services_data = ServiceRepository.get_all_available()
    return render_template('services.html', services=services_data)

@main_controller.route('/supermarket.html')
def supermarket():
    return render_template('supermarket.html')

@main_controller.route('/pharmacy.html')
def pharmacy():
    return render_template('pharmacy.html')

# =========================================================
# 3. AUTHENTICATION (Login/Register/Logout)
# =========================================================

@main_controller.route('/registration.html', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # 1. Get Form Data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # 2. Call Repository to Create User
        if UserRepository.create_user(username, email, password, phone=phone, address=address):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('main_controller.login'))
        else:
            flash('Registration failed. Email might already exist.', 'danger')
    
    return render_template('registration.html')

@main_controller.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 1. Find User by Email
        user = UserRepository.get_by_email(email)

        # 2. Verify Password
        if user and user.check_password(password):
            # 3. Create Session
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main_controller.home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@main_controller.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_controller.login'))

# =========================================================
# 4. USER PROFILE (FIXED)
# =========================================================

@main_controller.route('/profile')
@main_controller.route('/user_profile.html')
def user_profile():
    # 1. Check if logged in
    if 'user_id' not in session:
        flash('Please login to view your profile.', 'warning')
        return redirect(url_for('main_controller.login'))
    
    # 2. Prepare data for the HTML
    # In a real app, you would fetch these details from the database using session['user_id']
    # For now, we use the session username and dummy data for the rest to prevent crashes.
    
    current_name = session.get('username', 'Valued User')
    current_age = "65"  # You can fetch this from DB later
    current_email = "user@example.com" # You can fetch this from DB later
    
    # 3. Render template with ALL variables required by user_profile.html
    return render_template('user_profile.html', 
                           name=current_name, 
                           age=current_age, 
                           email=current_email)

# =========================================================
# 5. SPECIFIC SERVICE ROUTES (FIXED)
# =========================================================

@main_controller.route('/NurseRequest.html')
def nurse_request():
    service_id = request.args.get('s_id', 1)
    return render_template('NurseRequest.html', service_id=service_id)

@main_controller.route('/DoctorCheckup.html')
def doctor_checkup():
    service_id = request.args.get('s_id', 2)
    return render_template('DoctorCheckup.html', service_id=service_id)

@main_controller.route('/NeedCompany.html')
def need_company():
    service_id = request.args.get('s_id', 3)
    return render_template('NeedCompany.html', service_id=service_id)

# --- FIXED CAR WASHING ROUTE ---
@main_controller.route('/car-washing')
@main_controller.route('/CarWashing.html')
def car_washing():
    # Handles both the link in navbar and direct file access
    service_id = request.args.get('s_id', 4)
    return render_template('CarWashing.html', service_id=service_id)

# =========================================================
# 6. BOOKING LOGIC (Legacy & New)
# =========================================================

@main_controller.route('/book/<int:service_id>')
def book_service_redirect(service_id):
    if 'user_id' not in session:
        flash('Please login to book a service.', 'warning')
        return redirect(url_for('main_controller.login'))

    # Redirect to specific forms based on ID
    if service_id == 1:
        return redirect(url_for('main_controller.nurse_request', s_id=service_id))
    elif service_id == 2:
        return redirect(url_for('main_controller.doctor_checkup', s_id=service_id))
    elif service_id == 3:
        return redirect(url_for('main_controller.need_company', s_id=service_id))
    elif service_id == 4:
        return redirect(url_for('main_controller.car_washing', s_id=service_id))
    else:
        return redirect(url_for('main_controller.book_service', service_id=service_id))

@main_controller.route('/book-service/<int:service_id>', methods=['GET', 'POST'])
def book_service(service_id):
    service = ServiceRepository.get_by_id(service_id)
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        date = request.form.get('appointment_date')
        location = request.form.get('location')
        
        if AppointmentRepository.create_appointment(user_id, service_id, date, location):
            return render_template('book_service.html', service=service, success=True)
        else:
            return render_template('book_service.html', service=service, error_message="Database error")

    return render_template('book_service.html', service=service)

# =========================================================
# 7. PAYMENT & CONFIRMATION (UPDATED FOR CAR WASH)
# =========================================================

@main_controller.route('/payment', methods=['GET', 'POST'])
def payment():
    # 1. Capture data (Works for both GET and POST)
    service_name = request.values.get('serviceName', 'General Service')
    
    # 2. Price Logic
    # If it is Car Washing, we calculate price based on the selected package (duration)
    # If it is another service, we take the default price
    
    if service_name == 'Car Washing':
        package = request.values.get('duration') # Gets value from <select name="duration">
        
        if package == 'basic': price = '150'
        elif package == 'standard': price = '250'
        elif package == 'premium': price = '400'
        elif package == 'deluxe': price = '600'
        else: price = '150' # Default fallback
        
        # Optional: You could also add logic here to add extra costs for checkboxes
        
    else:
        # For Nurse, Doctor, etc.
        price = request.values.get('servicePrice', '0')

    # 3. Generate Random Order ID
    year = datetime.now().year
    rand_num = random.randint(1000, 9999)
    order_id = f"EC-{year}-{rand_num}"

    # 4. Render Confirmation
    return render_template('Confirmation.html', 
                           service_name=service_name, 
                           price=price,
                           order_id=order_id,
                           payment_method="Cash on Delivery")
    
@main_controller.route('/feedback')
def feedback():
    # This will prevent the crash when clicking "Leave Feedback"
    return render_template('index.html') # Or a feedback.html if you have one

@main_controller.route('/submit_booking', methods=['POST'])
def submit_booking():
    # This redirects the old name to your new payment logic
    return payment()