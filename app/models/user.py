import logging
from flask_login import UserMixin
from app import get_db_connection


class User(UserMixin):

    def __init__(self, user_id=None, name=None, email=None, password=None,
                 role='Elderly', phone_number=None, address=None, profile=None,
                 created_at=None, updated_at=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.phone_number = phone_number
        self.address = address
        self.profile = profile
        self.created_at = created_at
        self.updated_at = updated_at

    def get_id(self):
        return str(self.user_id)

    def is_admin(self):
        return self.role == 'Admin'

    def is_employee(self):
        return self.role in ['Staff', 'Doctor', 'Caregiver']

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [User] WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row.user_id,
                    name=row.name,
                    email=row.email,
                    password=row.password,
                    role=row.role,
                    phone_number=row.phone_number,
                    address=row.address,
                    profile=row.profile,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [User] WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row.user_id,
                    name=row.name,
                    email=row.email,
                    password=row.password,
                    role=row.role,
                    phone_number=row.phone_number,
                    address=row.address,
                    profile=row.profile,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
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
            cursor.execute("SELECT * FROM [User] ORDER BY user_id")
            users = []
            for row in cursor.fetchall():
                users.append(User(
                    user_id=row.user_id,
                    name=row.name,
                    email=row.email,
                    password=row.password,
                    role=row.role,
                    phone_number=row.phone_number,
                    address=row.address,
                    profile=row.profile,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                ))
            return users
        finally:
            conn.close()

    @staticmethod
    def get_employees():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM [User]
                WHERE role IN ('Staff', 'Doctor', 'Caregiver')
                ORDER BY role, name
            """)
            employees = []
            for row in cursor.fetchall():
                employees.append(User(
                    user_id=row.user_id,
                    name=row.name,
                    email=row.email,
                    password=row.password,
                    role=row.role,
                    phone_number=row.phone_number,
                    address=row.address,
                    profile=row.profile,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                ))
            return employees
        finally:
            conn.close()

    @staticmethod
    def count_by_role(role):
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [User] WHERE role = ?", (role,))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()

    @staticmethod
    def count_all():
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [User]")
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
                INSERT INTO [User] (name, email, password, role, phone_number, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.name, self.email, self.password, self.role,
                  self.phone_number, self.address))
            conn.commit()

            cursor.execute("SELECT @@IDENTITY")
            result = cursor.fetchone()
            self.user_id = result[0] if result else None
            return True
        except Exception as e:
            logging.error(f"Error saving user: {e}")
            return False
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            if self.password:
                cursor.execute("""
                    UPDATE [User]
                    SET name=?, email=?, password=?, role=?, phone_number=?, address=?, updated_at=GETDATE()
                    WHERE user_id=?
                """, (self.name, self.email, self.password, self.role,
                      self.phone_number, self.address, self.user_id))
            else:
                cursor.execute("""
                    UPDATE [User]
                    SET name=?, email=?, role=?, phone_number=?, address=?, updated_at=GETDATE()
                    WHERE user_id=?
                """, (self.name, self.email, self.role,
                      self.phone_number, self.address, self.user_id))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM [User] WHERE user_id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'
