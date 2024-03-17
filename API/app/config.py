"""
This file stores configuration variables
for the Flask application.
"""
from app.models.user import User

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
    "User": User
}
