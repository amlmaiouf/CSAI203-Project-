from core.db_singelton import db
from models.appointment import Appointment

class AppointmentRepository:
    """
    Repository for Appointment Logic.
    Handles booking and automatic staff notifications.
    """

    @staticmethod
    def create_appointment(user_id, service_id, appointment_date, location):
        """
        Creates an appointment and notifies all staff members.
        (Replaces the old logic from db.py)
        """
        conn = db.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            
            # 1. Insert Appointment
            query_appt = """
                INSERT INTO Appointment (user_id, service_id, appointment_date, location)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query_appt, (user_id, service_id, appointment_date, location))
            
            # 2. Get all Staff IDs
            query_staff = "SELECT user_id FROM [User] WHERE role='Staff'"
            cursor.execute(query_staff)
            staff_users = cursor.fetchall()
            
            # 3. Create Notifications for each staff member
            query_notify = """
                INSERT INTO Notification (user_id, title, message, type)
                VALUES (?, ?, ?, 'Appointment')
            """
            
            notification_title = f'New appointment for service {service_id}'
            notification_msg = f'User {user_id} booked on {appointment_date}'
            
            for staff in staff_users:
                cursor.execute(query_notify, (staff.user_id, notification_title, notification_msg))
            
            # 4. Commit everything at once (Transaction)
            conn.commit()
            print(f"SUCCESS: Appointment created for User {user_id}")
            return True

        except Exception as e:
            # If anything fails, rollback changes so we don't have partial data
            conn.rollback()
            print(f"ERROR: Could not create appointment: {e}")
            return False