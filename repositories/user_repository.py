from core.db_singelton import db
from models.user import User
from werkzeug.security import generate_password_hash

class UserRepository:
    """
    Repository for User Management (Login/Register).
    """

    @staticmethod
    def create_user(username, email, password, role='Client', phone=None, address=None):
        """Registers a new user with a hashed password."""
        conn = db.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            hashed_pw = generate_password_hash(password)

            query = """
                INSERT INTO [User] (username, email, password_hash, role, phone, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (username, email, hashed_pw, role, phone, address))
            conn.commit()
            return True
        except Exception as e:
            print(f"ERROR: Could not register user: {e}")
            return False

    @staticmethod
    def get_by_email(email):
        """Finds a user by email (for Login)."""
        conn = db.get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        query = "SELECT user_id, username, email, password_hash, role, phone, address FROM [User] WHERE email = ?"
        cursor.execute(query, (email,))
        row = cursor.fetchone()

        if row:
            return User(
                user_id=row.user_id,
                username=row.username,
                email=row.email,
                password_hash=row.password_hash,
                role=row.role,
                phone=row.phone,
                address=row.address
            )
        return None

    @staticmethod
    def get_by_id(user_id):
        """Finds a user by ID (for Session Management)."""
        conn = db.get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        query = "SELECT user_id, username, email, password_hash, role, phone, address FROM [User] WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if row:
            return User(
                user_id=row.user_id,
                username=row.username,
                email=row.email,
                password_hash=row.password_hash,
                role=row.role,
                phone=row.phone,
                address=row.address
            )
        return None