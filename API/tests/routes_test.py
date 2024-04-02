import unittest
from app.views import app_views as app
from app import storage
from app.models.user import User

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True


    def account_test(self):
        response = self.app.post('/api/sign_up', data={
                "first_name": "omar",
                "last_name": "id hmaid",
                "email": "omaridhmaid@gmial.com",
                "password": "omarIDH0.2",
                "birth_date": "2002-01-07",
                "location": "Morocco Massa",
                "picture": "none"}, follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual("User signed up successfully", response.data.get('message'))

        """check user exists"""
        user = storage.session.query(User).filter_by(email="omaridhmaid@gmial.com").first()
        self.assertEqual(user.first_name, "omar")

        """testing validation functionality"""
        response = self.app.put(f'/api/validation/{user.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual("account has been validated", response.data.get('message'))

        """check user verify"""
        self.assertEqual(user.verify, True)

    def session_test(self):
        """check log in"""
        response = self.app.post('/api/login', data={
                "email": "omaridhmaid@gmial.com",
                "password": "omarIDH0.2"}, follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual("logged in", response.data.get('message'))


        """check log out"""
        response = self.app.delete('/api/logout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual("logged out", response.data.get('message'))



if __name__ == '__main__':
    unittest.main()
