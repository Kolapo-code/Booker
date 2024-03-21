"""
This file stores configuration variables
for the Flask application.
"""
from app.models.regular_user import RegularUser
from app.models.premium_account import PremiumAccount
from app.models.session import Session

class DBConfig:
    user = "admin"
    passworld = "admin"
    host = "localhost"
    database = "booker"
    @property
    def url(self):
        # print('hey, am here')
        return f"mysql+mysqlconnector://{self.user}:{self.passworld}@{self.host}/{self.database}"


classes = {
    "RegularUser": RegularUser,
    "PremiumAccount": PremiumAccount,
    "Session": Session
}

EXPIRY = 3600 * 24
