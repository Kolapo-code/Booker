"""
This file stores configuration variables
for the Flask application.
"""

from app.models.admin_account import AdminAccount

from app.models.user import User
from app.models.premium_account import PremiumAccount
from app.models.session import Session
from app.models.workspace import Workspace
from app.models.appointment import Appointment
from app.models.temporary_password import TemporaryPassword
from app.models.review import Review
from app.models.reclaim import Reclaim
import json


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
    "User": User,
    "AdminAccount": AdminAccount,
    "PremiumAccount": PremiumAccount,
    "Appointment": Appointment,
    "Session": Session,
    "TemporaryPassword": TemporaryPassword,
    "Workspace": Workspace,
    "Review": Review,
    "Reclaim": Reclaim,
}

EXPIRY = 3600 * 24
