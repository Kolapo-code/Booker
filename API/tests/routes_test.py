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
        self.assertEqual('user created successfully', response.data.get('message'))

        """check user exists"""
        user = storage.session.query(User).filter_by(email="omaridhmaid@gmial.com").first()
        self.assertEqual(user.first_name, "omar")


if __name__ == '__main__':
    unittest.main()
