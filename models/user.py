from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id, username, email, password_hash, role='Client', phone=None, address=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.phone = phone
        self.address = address

    def check_password(self, password):
        """Checks if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }