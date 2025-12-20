import pyodbc
from datetime import datetime

def get_db_connection():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=ASUS;"
        "Database=elderly_care_system;"
        "Trusted_Connection=yes;"
    )
    return conn
'''
# FR2: Fetch all available services
def fetch_services():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT service_id, service_name, type, price, description, is_available
        FROM Service
        WHERE is_available = 1
    """)
    services = cursor.fetchall()
    conn.close()
    return services

# FR3: Fetch single service by ID
def fetch_service(service_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT service_id, service_name, type, price, description
        FROM Service
        WHERE service_id = ?
    """, (service_id,))
    service = cursor.fetchone()
    conn.close()
    return service

# FR3: Create appointment and notify staff
def create_appointment(user_id, service_id, appointment_date, location):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert appointment
    cursor.execute("""
        INSERT INTO Appointment (user_id, service_id, appointment_date, location)
        VALUES (?, ?, ?, ?)
    """, (user_id, service_id, appointment_date, location))
    conn.commit()

    # Notify all staff
    cursor.execute("SELECT user_id FROM [User] WHERE role='Staff'")
    staff_users = cursor.fetchall()
    for staff in staff_users:
        cursor.execute("""
            INSERT INTO Notification (user_id, title, message, type)
            VALUES (?, ?, ?, 'Appointment')
        """, (staff.user_id,
              f'New appointment for service {service_id}',
              f'User {user_id} booked an appointment on {appointment_date}'))
    conn.commit()
    conn.close()
    '''