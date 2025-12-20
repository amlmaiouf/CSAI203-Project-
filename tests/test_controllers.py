import unittest
from core import create_app

class TestMainController(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_supermarket_loads(self):
        """Test if Supermarket page is accessible"""
        response = self.client.get('/supermarket.html')
        self.assertEqual(response.status_code, 200)

    def test_pharmacy_loads(self):
        """Test if Pharmacy page is accessible"""
        response = self.client.get('/pharmacy.html')
        self.assertEqual(response.status_code, 200)

    def test_services_list_loads(self):
        """Test if the main services menu loads"""
        response = self.client.get('/services.html')
        self.assertEqual(response.status_code, 200)