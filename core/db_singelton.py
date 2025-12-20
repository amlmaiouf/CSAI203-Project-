import pyodbc

class Database:
    """
    Singleton Database Class (Bonus #4).
    Manages the PyODBC connection to SQL Server.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = None
        return cls._instance

    def init_app(self, app):
        """Initializes the connection using values from app.config"""
        self.driver = app.config.get('DB_DRIVER')
        self.server = app.config.get('DB_SERVER')
        self.database = app.config.get('DB_DATABASE')
        self.trusted = app.config.get('DB_TRUSTED_CONNECTION')

    def get_connection(self):
        """Returns the current connection or creates a new one if missing."""
        if self.conn is None:
            try:
                # Construct connection string dynamically
                conn_str = (
                    f"Driver={self.driver};"
                    f"Server={self.server};"
                    f"Database={self.database};"
                    f"Trusted_Connection={self.trusted};"
                )
                self.conn = pyodbc.connect(conn_str)
                print("SUCCESS: Database connection established.")
            except Exception as e:
                print(f"ERROR: DB Connection failed: {e}")
                return None
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

# Create the global instance
db = Database()