from core.db_singleton import Database

class PaymentModel:
    def __init__(self):
        self.db = Database()

    def create_order(self, service_name, customer_name, phone, email, date, duration, total_price, payment_method):
        cursor = self.db.get_cursor()
        cursor.execute("""
            INSERT INTO orders 
            (service_name, customer_name, phone, email, date, duration, total_price, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (service_name, customer_name, phone, email, date, duration, total_price, payment_method))
        self.db.commit()
