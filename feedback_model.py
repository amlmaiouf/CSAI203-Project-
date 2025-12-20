from core.db_singleton import Database

class FeedbackModel:
    def __init__(self):
        self.db = Database()

    def create_feedback(self, service_name, rating, user_name, comment):
        cursor = self.db.get_cursor()
        cursor.execute("""
            INSERT INTO feedbacks (service_name, rating, user_name, comment)
            VALUES (%s, %s, %s, %s)
        """, (service_name, rating, user_name, comment))
        self.db.commit()

    def get_all_feedback(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM feedbacks ORDER BY created_at DESC")
        return cursor.fetchall()
