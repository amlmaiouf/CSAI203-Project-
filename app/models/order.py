import logging
from app import get_db_connection


class Order:

    VALID_STATUSES = ['Pending', 'Confirmed', 'In Progress', 'Completed', 'Cancelled']

    def __init__(self, order_id=None, user_id=None, order_date=None, status='Pending',
                 total_price=0, delivery_address=None, notes=None,
                 created_at=None, updated_at=None):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.status = status
        self.total_price = total_price
        self.delivery_address = delivery_address
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        self.customer_name = None
        self.customer_email = None

    @staticmethod
    def get_by_id(order_id):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, u.name as customer_name, u.email as customer_email
                FROM [Order] o
                JOIN [User] u ON o.user_id = u.user_id
                WHERE o.order_id = ?
            """, (order_id,))
            row = cursor.fetchone()
            if row:
                order = Order(
                    order_id=row.order_id,
                    user_id=row.user_id,
                    order_date=row.order_date,
                    status=row.status,
                    total_price=float(row.total_price),
                    delivery_address=row.delivery_address,
                    notes=row.notes,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
                order.customer_name = row.customer_name
                order.customer_email = row.customer_email
                return order
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, u.name as customer_name, u.email as customer_email
                FROM [Order] o
                JOIN [User] u ON o.user_id = u.user_id
                ORDER BY o.order_date DESC
            """)
            orders = []
            for row in cursor.fetchall():
                order = Order(
                    order_id=row.order_id,
                    user_id=row.user_id,
                    order_date=row.order_date,
                    status=row.status,
                    total_price=float(row.total_price),
                    delivery_address=row.delivery_address,
                    notes=row.notes,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
                order.customer_name = row.customer_name
                order.customer_email = row.customer_email
                orders.append(order)
            return orders
        finally:
            conn.close()

    @staticmethod
    def get_recent(limit=5):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.*, u.name as customer_name, u.email as customer_email
                FROM [Order] o
                JOIN [User] u ON o.user_id = u.user_id
                ORDER BY o.created_at DESC
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
            """, (limit,))
            orders = []
            for row in cursor.fetchall():
                order = Order(
                    order_id=row.order_id,
                    user_id=row.user_id,
                    order_date=row.order_date,
                    status=row.status,
                    total_price=float(row.total_price),
                    delivery_address=row.delivery_address,
                    notes=row.notes,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
                order.customer_name = row.customer_name
                order.customer_email = row.customer_email
                orders.append(order)
            return orders
        finally:
            conn.close()

    @staticmethod
    def count_all():
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [Order]")
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()

    @staticmethod
    def count_by_status(status):
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [Order] WHERE status = ?", (status,))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()

    def save(self):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO [Order] (user_id, order_date, status, total_price, delivery_address, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.user_id, self.order_date, self.status, self.total_price,
                  self.delivery_address, self.notes))
            conn.commit()

            cursor.execute("SELECT @@IDENTITY")
            result = cursor.fetchone()
            self.order_id = result[0] if result else None
            return True
        except Exception as e:
            logging.error(f"Error saving order: {e}")
            return False
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE [Order]
                SET user_id=?, order_date=?, status=?, total_price=?, delivery_address=?, notes=?, updated_at=GETDATE()
                WHERE order_id=?
            """, (self.user_id, self.order_date, self.status, self.total_price,
                  self.delivery_address, self.notes, self.order_id))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating order: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(order_id):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM [Order] WHERE order_id = ?", (order_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting order: {e}")
            return False
        finally:
            conn.close()

    def __repr__(self):
        return f'<Order {self.order_id}>'


class OrderService:

    def __init__(self, order_service_id=None, order_id=None, service_id=None,
                 quantity=1, price=0, created_at=None):
        self.order_service_id = order_service_id
        self.order_id = order_id
        self.service_id = service_id
        self.quantity = quantity
        self.price = price
        self.created_at = created_at


class Payment:

    VALID_STATUSES = ['Pending', 'Paid', 'Failed', 'Refunded']
    VALID_METHODS = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer']

    def __init__(self, payment_id=None, order_id=None, payment_status='Pending',
                 payment_method=None, payment_date=None, amount=0,
                 transaction_id=None, created_at=None):
        self.payment_id = payment_id
        self.order_id = order_id
        self.payment_status = payment_status
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.amount = amount
        self.transaction_id = transaction_id
        self.created_at = created_at


class Appointment:

    VALID_STATUSES = ['Scheduled', 'Confirmed', 'In Progress', 'Completed', 'Cancelled', 'No Show']

    def __init__(self, appointment_id=None, user_id=None, service_id=None,
                 staff_id=None, appointment_date=None, status='Scheduled',
                 location=None, notes=None, created_at=None, updated_at=None):
        self.appointment_id = appointment_id
        self.user_id = user_id
        self.service_id = service_id
        self.staff_id = staff_id
        self.appointment_date = appointment_date
        self.status = status
        self.location = location
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
