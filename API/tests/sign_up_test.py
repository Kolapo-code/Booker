import unittest
from app.views import app_views as app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Clean up after tests if needed
        pass

    def test_home_page(self):
        # Test the home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Flask App', response.data)

    def test_login(self):
        # Test the login functionality
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
