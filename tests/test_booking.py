import unittest
from core import create_app

class TestBookingLogic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_booking_redirect_nurse(self):
        """Test if service_id 1 redirects to NurseRequest"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            
        response = self.client.get('/book/1', follow_redirects=True)
            
        self.assertIn(b'Request a Nurse', response.data)

    def test_booking_redirect_carwash(self):
        """Test if service_id 4 redirects to CarWashing"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            
        response = self.client.get('/book/4', follow_redirects=True)
        self.assertIn(b'CarWashing.html', response.data)

    def test_booking_unauthorized(self):
        """Test that booking fails if user is not logged in"""
        response = self.client.get('/book/1', follow_redirects=True)
        
        self.assertIn(b'Login Page', response.data)