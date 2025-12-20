import logging
from app import get_db_connection


class Feedback:

    def __init__(self, feedback_id=None, user_id=None, service_id=None,
                 order_id=None, date=None, rating=0, comment=None, created_at=None):
        self.feedback_id = feedback_id
        self.user_id = user_id
        self.service_id = service_id
        self.order_id = order_id
        self.date = date
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.user_name = None
        self.service_name = None

    def get_rating_text(self):
        rating_texts = {
            1: 'Poor',
            2: 'Fair',
            3: 'Good',
            4: 'Very Good',
            5: 'Excellent'
        }
        return rating_texts.get(self.rating, 'Unknown')

    @staticmethod
    def get_by_id(feedback_id):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.*, u.name as user_name, s.service_name
                FROM [Feedback] f
                JOIN [User] u ON f.user_id = u.user_id
                JOIN [Service] s ON f.service_id = s.service_id
                WHERE f.feedback_id = ?
            """, (feedback_id,))
            row = cursor.fetchone()
            if row:
                fb = Feedback(
                    feedback_id=row.feedback_id,
                    user_id=row.user_id,
                    service_id=row.service_id,
                    order_id=row.order_id,
                    date=row.date,
                    rating=row.rating,
                    comment=row.comment,
                    created_at=row.created_at
                )
                fb.user_name = row.user_name
                fb.service_name = row.service_name
                return fb
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
                SELECT f.*, u.name as user_name, s.service_name
                FROM [Feedback] f
                JOIN [User] u ON f.user_id = u.user_id
                JOIN [Service] s ON f.service_id = s.service_id
                ORDER BY f.created_at DESC
            """)
            feedback_list = []
            for row in cursor.fetchall():
                fb = Feedback(
                    feedback_id=row.feedback_id,
                    user_id=row.user_id,
                    service_id=row.service_id,
                    order_id=row.order_id,
                    date=row.date,
                    rating=row.rating,
                    comment=row.comment,
                    created_at=row.created_at
                )
                fb.user_name = row.user_name
                fb.service_name = row.service_name
                feedback_list.append(fb)
            return feedback_list
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        return Feedback.get_filtered(user_id=user_id)

    @staticmethod
    def get_filtered(service_id=None, rating=None, user_id=None):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            query = """
                SELECT f.*, u.name as user_name, s.service_name
                FROM [Feedback] f
                JOIN [User] u ON f.user_id = u.user_id
                JOIN [Service] s ON f.service_id = s.service_id
                WHERE 1=1
            """
            params = []

            if service_id:
                query += " AND f.service_id = ?"
                params.append(service_id)

            if rating:
                query += " AND f.rating = ?"
                params.append(rating)

            if user_id:
                query += " AND f.user_id = ?"
                params.append(user_id)

            query += " ORDER BY f.created_at DESC"

            cursor.execute(query, params)
            feedback_list = []
            for row in cursor.fetchall():
                fb = Feedback(
                    feedback_id=row.feedback_id,
                    user_id=row.user_id,
                    service_id=row.service_id,
                    order_id=row.order_id,
                    date=row.date,
                    rating=row.rating,
                    comment=row.comment,
                    created_at=row.created_at
                )
                fb.user_name = row.user_name
                fb.service_name = row.service_name
                feedback_list.append(fb)
            return feedback_list
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
                SELECT f.*, u.name as user_name, s.service_name
                FROM [Feedback] f
                JOIN [User] u ON f.user_id = u.user_id
                JOIN [Service] s ON f.service_id = s.service_id
                ORDER BY f.created_at DESC
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
            """, (limit,))
            feedback_list = []
            for row in cursor.fetchall():
                fb = Feedback(
                    feedback_id=row.feedback_id,
                    user_id=row.user_id,
                    service_id=row.service_id,
                    order_id=row.order_id,
                    date=row.date,
                    rating=row.rating,
                    comment=row.comment,
                    created_at=row.created_at
                )
                fb.user_name = row.user_name
                fb.service_name = row.service_name
                feedback_list.append(fb)
            return feedback_list
        finally:
            conn.close()

    @staticmethod
    def count_all():
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [Feedback]")
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()

    @staticmethod
    def count_by_rating(rating):
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [Feedback] WHERE rating = ?", (rating,))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()

    @staticmethod
    def get_average_rating():
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT AVG(CAST(rating AS FLOAT)) FROM [Feedback]")
            row = cursor.fetchone()
            result = row[0] if row else None
            return round(result, 2) if result else 0
        finally:
            conn.close()

    @staticmethod
    def delete(feedback_id):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM [Feedback] WHERE feedback_id = ?", (feedback_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting feedback: {e}")
            return False
        finally:
            conn.close()

    def save(self):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO [Feedback] (user_id, service_id, order_id, date, rating, comment)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.user_id, self.service_id, self.order_id, self.date, self.rating, self.comment))
            conn.commit()

            cursor.execute("SELECT @@IDENTITY")
            result = cursor.fetchone()
            self.feedback_id = result[0] if result else None
            return True
        except Exception as e:
            logging.error(f"Error saving feedback: {e}")
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
                UPDATE [Feedback]
                SET user_id=?, service_id=?, order_id=?, date=?, rating=?, comment=?
                WHERE feedback_id=?
            """, (self.user_id, self.service_id, self.order_id, self.date,
                  self.rating, self.comment, self.feedback_id))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating feedback: {e}")
            return False
        finally:
            conn.close()

    def __repr__(self):
        return f'<Feedback {self.feedback_id} - Rating: {self.rating}>'


class Notification:

    VALID_TYPES = ['Order', 'Appointment', 'Payment', 'System', 'Reminder']

    def __init__(self, notification_id=None, user_id=None, title=None,
                 message=None, type=None, is_read=False, created_at=None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type
        self.is_read = is_read
        self.created_at = created_at


class ServiceHistory:

    VALID_STATUSES = ['Requested', 'In Progress', 'Completed', 'Cancelled']

    def __init__(self, history_id=None, user_id=None, service_id=None,
                 order_id=None, request_date=None, completion_date=None,
                 status='Requested', notes=None, created_at=None):
        self.history_id = history_id
        self.user_id = user_id
        self.service_id = service_id
        self.order_id = order_id
        self.request_date = request_date
        self.completion_date = completion_date
        self.status = status
        self.notes = notes
        self.created_at = created_at
