from core.db_singelton import db
from models.service import Service

class ServiceRepository:
    """
    Repository for Service Database Operations.
    Isolates SQL queries from the Controller.
    """
    
    @staticmethod
    def get_all_available():
        """Fetches all available services (Replaces old fetch_services)"""
        conn = db.get_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        query = """
            SELECT service_id, service_name, type, price, description, is_available
            FROM Service
            WHERE is_available = 1
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert raw SQL rows into Service objects
        services = []
        for row in rows:
            # Assuming row order matches query order
            services.append(Service(
                service_id=row.service_id,
                service_name=row.service_name,
                type=row.type,
                price=row.price,
                description=row.description,
                is_available=row.is_available
            ))
        return services

    @staticmethod
    def get_by_id(service_id):
        """Fetches a single service by ID (Replaces old fetch_service)"""
        conn = db.get_connection()
        if not conn:
            return None
            
        cursor = conn.cursor()
        query = """
            SELECT service_id, service_name, type, price, description, is_available
            FROM Service
            WHERE service_id = ?
        """
        cursor.execute(query, (service_id,))
        row = cursor.fetchone()
        
        if row:
            return Service(
                service_id=row.service_id,
                service_name=row.service_name,
                type=row.type,
                price=row.price,
                description=row.description,
                is_available=row.is_available
            )
        return None