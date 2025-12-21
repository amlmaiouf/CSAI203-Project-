import unittest
from core.db_singelton import Database, db
from core import create_app

class TestDatabaseSingleton(unittest.TestCase):
    def setUp(self):
        # We need the app context to initialize the DB config
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_singleton_instance(self):
        """Test that two instances of Database are actually the same object."""
        db1 = Database()
        db2 = Database()
        self.assertIs(db1, db2, "Database class is not a Singleton!")

    def test_connection_established(self):
        """Test if the Singleton successfully creates a pyodbc connection."""
        connection = db.get_connection()
        self.assertIsNotNone(connection, "Failed to connect to SQL Server. Check your config.py!")
        self.assertTrue(hasattr(connection, 'cursor'), "Connection object is missing cursor method.")

if __name__ == '__main__':
    unittest.main()