from datetime import datetime

class Appointment:
    def __init__(self, user_id, service_id, appointment_date, location, status='Pending'):
        self.user_id = user_id
        self.service_id = service_id
        self.appointment_date = appointment_date
        self.location = location
        self.status = status
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'service_id': self.service_id,
            'appointment_date': self.appointment_date,
            'location': self.location,
            'status': self.status
        }