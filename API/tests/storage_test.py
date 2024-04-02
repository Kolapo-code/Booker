from app.models.base_model import BaseModel
from app.models.user import User
import unittest


class TestUser(unittest.TestCase):
    """Testing the user model."""

    def test_instance(self):
        """Test the instance user."""
        user = User(
			birth_date=[1999, 9, 1],
			email="bookerapiteam@gmail.com",
			first_name="Booker",
			last_name="Api",
			location="Morocco",
			picture="",
			password="Booker"
		)
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_password(self):
        """Test the instance user."""
        user = User(
			birth_date=[1999, 9, 1],
			email="bookerapiteam@gmail.com",
			first_name="Booker",
			last_name="Api",
			location="Morocco",
			picture="",
			password="Booker"
		)
        self.assertEqual(user.password, "You can not get the password it is indeed private")
        new_password = "Booker"
        # user.password(new_password)
        self.assertTrue(user.check_password(new_password)) # Something is wrong here, it returns False.
