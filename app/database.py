import pyodbc


DB_CONFIG = {
    'server': r'LAPTOP-CIOQ170I\SQLEXPRESS',
    'database': 'elderly_care_system',
    'driver': '{ODBC Driver 17 for SQL Server}',
    # 'driver': '{SQL Server};',
    'trusted_connection': 'yes',
}


def get_db_connection():
    try:
        conn_str = (
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"Trusted_Connection=yes;"
        )

        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None
