"""
Service Model - Elderly Care System
Uses pyodbc to connect to SQL Server
"""

from app import get_db_connection


class Service:
    """Service Model for managing available services"""
    
    VALID_TYPES = [
        'Medical', 'Housekeeping', 'Grocery', 'Pharmacy', 
        'Pet Care', 'Car Cleaning', 'Nursing', 'Delivery', 'Companionship'
    ]
    
    def __init__(self, service_id=None, service_name=None, type=None, price=0,
                 description=None, is_available=True, created_at=None, updated_at=None):
        self.service_id = service_id
        self.service_name = service_name
        self.type = type
        self.price = price
        self.description = description
        self.is_available = is_available
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def get_by_id(service_id):
        """Get service by ID"""
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [Service] WHERE service_id = ?", (service_id,))
            row = cursor.fetchone()
            if row:
                return Service(
                    service_id=row.service_id,
                    service_name=row.service_name,
                    type=row.type,
                    price=float(row.price),
                    description=row.description,
                    is_available=row.is_available,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """Get all services"""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [Service] ORDER BY service_id")
            services = []
            for row in cursor.fetchall():
                svc = Service(
                    service_id=row.service_id,
                    service_name=row.service_name,
                    type=row.type,
                    price=float(row.price),
                    description=row.description,
                    is_available=row.is_available,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                )
                services.append(svc)
            return services
        finally:
            conn.close()
    
    @staticmethod
    def get_available():
        """Get all available services"""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [Service] WHERE is_available = 1 ORDER BY service_id")
            services = []
            for row in cursor.fetchall():
                services.append(Service(
                    service_id=row.service_id,
                    service_name=row.service_name,
                    type=row.type,
                    price=float(row.price),
                    description=row.description,
                    is_available=row.is_available,
                    created_at=row.created_at,
                    updated_at=row.updated_at
                ))
            return services
        finally:
            conn.close()
    
    @staticmethod
    def count_all():
        """Count all services"""
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [Service]")
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def get_request_count(self):
        """Get total number of requests for this service"""
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM [Order_Service] WHERE service_id = ?
            """, (self.service_id,))
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def get_average_rating(self):
        """Get average rating for this service"""
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(CAST(rating AS FLOAT)) FROM [Feedback] WHERE service_id = ?
            """, (self.service_id,))
            result = cursor.fetchone()[0]
            return round(result, 2) if result else 0
        finally:
            conn.close()
    
    def get_feedback_count(self):
        """Get feedback count for this service"""
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM [Feedback] WHERE service_id = ?
            """, (self.service_id,))
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def get_revenue(self):
        """Get total revenue for this service"""
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(price * quantity), 0) 
                FROM [Order_Service] WHERE service_id = ?
            """, (self.service_id,))
            result = cursor.fetchone()[0]
            return float(result) if result else 0
        finally:
            conn.close()
    
    def get_recent_feedback(self, limit=5):
        """Get recent feedback for this service"""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.*, u.name as user_name 
                FROM [Feedback] f
                JOIN [User] u ON f.user_id = u.user_id
                WHERE f.service_id = ?
                ORDER BY f.created_at DESC
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
            """, (self.service_id, limit))
            feedback_list = []
            for row in cursor.fetchall():
                feedback_list.append({
                    'feedback_id': row.feedback_id,
                    'user_name': row.user_name,
                    'rating': row.rating,
                    'comment': row.comment,
                    'date': row.date,
                    'created_at': row.created_at
                })
            return feedback_list
        finally:
            conn.close()
    
    def save(self):
        """Insert new service"""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO [Service] (service_name, type, price, description, is_available)
                VALUES (?, ?, ?, ?, ?)
            """, (self.service_name, self.type, self.price, self.description, 
                  1 if self.is_available else 0))
            conn.commit()
            
            cursor.execute("SELECT @@IDENTITY")
            self.service_id = cursor.fetchone()[0]
            return True
        except Exception as e:
            print(f"Error saving service: {e}")
            return False
        finally:
            conn.close()
    
    def update(self):
        """Update existing service"""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE [Service] 
                SET service_name=?, type=?, price=?, description=?, is_available=?, updated_at=GETDATE()
                WHERE service_id=?
            """, (self.service_name, self.type, self.price, self.description, 
                  1 if self.is_available else 0, self.service_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating service: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def toggle_availability(service_id):
        """Toggle service availability"""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE [Service] 
                SET is_available = CASE WHEN is_available = 1 THEN 0 ELSE 1 END,
                    updated_at = GETDATE()
                WHERE service_id = ?
            """, (service_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error toggling service: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def delete(service_id):
        """Delete service by ID"""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM [Service] WHERE service_id = ?", (service_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting service: {e}")
            return False
        finally:
            conn.close()
    
    def __repr__(self):
        return f'<Service {self.service_name}>'
