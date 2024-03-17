"""
This file stores configuration variables
for the Flask application.
"""
from app.models.user import User

class DBConfig:
    user = "admin"
    passworld = "admin"
    host = "localhost"
    data_base = "booker"
    url = f"mysql+mysqldb://{user}:{passworld}@{host}/{data_base}"


classes = {
    "user": User
}