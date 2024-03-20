from app.models.regular_user import RegularUser
from datetime import datetime
from flask import abort
from uuid import uuid4
from app import auth
import base64
from app.utils.helper import verify_email


def post_user(data):
    """A function that creates a new user."""
    data_list = [
        "first_name",
        "last_name",
        "email",
        "password",
        "birth_date",
        "location",
    ]
    user_data = {}
    for key in data_list:
        if key not in data:
            abort(400, description=f"{key} does not exits in the given data")
        if key == "birth_date":
            if not isinstance(data[key], list) or len(data[key]) != 3:
                print("wrong date")
                abort(403, "Birthdate should be in this format [Y, M, D]")
            user_data[key] = datetime(*data[key])
            continue
        if key == "email":
            if not data[key] and not isinstance(data[key], str):
                abort(400, description=f"{data[key]} is not valid")
        if key == "password":
            user_data[key] = base64.b64encode(data[key].encode("utf-8"))
            continue
        user_data[key] = data[key]
    if auth.check_email(user_data["email"]):
        abort(
            403,
            description="The provided email already exists. Try to log in or change the email.",
        )
    token = str(uuid4())
    user_data["token"] = token
    user = RegularUser(**user_data)
    user.save()
    verify_email(user.first_name, user.email, f"Booker.com/validation/{token}")
    return user.id

def put_validation(users):
    """A function that validates the token send to the email of the user."""
    user = list(users.values())[0]
    user.valid = True
    user.token = None
    user.save()
