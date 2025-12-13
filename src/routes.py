from app import app
from flask import render_template, request, redirect, url_for
from db import fetch_services, fetch_service, create_appointment
from datetime import datetime

@app.route('/')
def home():
    # Redirect root URL to /services
    return redirect(url_for('view_services'))

# FR2: Serve all available services
@app.route('/services')
def view_services():
    services = fetch_services()
    services_list = []
    for s in services:
        services_list.append({
            'service_id': s.service_id,
            'service_name': s.service_name,
            'type': s.type,
            'price': float(s.price),
            'description': s.description
        })
    return render_template('services.html', services=services_list)

# FR3: Book appointment
@app.route('/book/<int:service_id>', methods=['GET', 'POST'])
def book_service(service_id):
    service = fetch_service(service_id)
    success = False  # Flag for booking success
    error_message = None

    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            appointment_date_str = request.form['appointment_date']  # string from form
            location = request.form['location']

            # Convert to datetime object (SQL Server friendly)
            appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d")

            # Create appointment
            create_appointment(user_id, service_id, appointment_date, location)
            success = True

        except ValueError:
            error_message = "Invalid date format. Use YYYY-MM-DD"
        except Exception as e:
            error_message = str(e)

    return render_template(
        'book_service.html',
        service=service,
        success=success,
        error_message=error_message
    )
# Static pages routes
@app.route('/nurserequest')
def nurse_request():
    return render_template('NurseRequest.html')

@app.route('/doctorcheckup')
def doctor_checkup():
    return render_template('DoctorCheckup.html')

@app.route('/needcompany')
def need_company():
    return render_template('NeedCompany.html')

@app.route('/carwashing')
def car_washing():
    return render_template('CarWashing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')
