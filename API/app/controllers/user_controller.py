from app.models.user import User
from datetime import datetime
from flask import abort, request
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
    if auth.check_email(user_data["email"]) is not None:
        abort(
            403,
            description="The provided email already exists. Try to log in or change the email.",
        )
    token = str(uuid4())
    user_data["token"] = token
    user = User(**user_data)
    user.save()
    verify_email(user.first_name, user.email, f"Booker.com/validation/{token}")
    return user.id

def put_validation(users):
    """A function that validates the token send to the email of the user."""
    user = list(users.values())[0]
    user.valid = True
    user.token = None
    user.save()

def verify_login(data):
    session_id = auth.get_session_id(request)
    if session_id is not None and auth.check_session(session_id):
        abort(403, "user already logged in")
    if 'email' not in data or 'password' not in data:
        abort(400)
    email = data['email']
    password = data['password']
    user = auth.check_email(email)
    if user is None:
        abort(403, 'email not found please sign up')
    if not user.check_password(base64.b64encode(password.encode('utf-8'))):
        abort(403, 'password is incorrect')
    if not user.valid:
        abort(403, 'email is not yet validated')
    session_id = auth.create_session(user.id)
    if session_id is None:
        abort(403, 'there has been error while creating the session')
    return session_id

def verify_logout(request):
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, 'no session exists')
    session = auth.get_session(session_id)
    auth.delete_session(session)
