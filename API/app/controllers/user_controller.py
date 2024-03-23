from app.models.user import User
from app.models.temporary_password import TemporaryPassword
from datetime import datetime
from flask import abort, request
from uuid import uuid4
from app import auth, storage
import re
import base64
from app.utils.helper import verify_email
from app.utils.helper_ import send_password, generate_password



def post_user(data):
    """A function that creates a new user after checking all the data requirements."""
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
                abort(403, "Birthdate should be in this format [Y, M, D]")
            user_data[key] = datetime(*data[key])
            continue
        if key == "email":
            if not isinstance(data[key], str) or not re.search(
                "^[\w_\-.0-9]+@\w+\.\w+$", data[key]
            ):
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
    """A function that validates the token that has been send to the email of the user."""
    user = list(users.values())[0]
    user.valid = True
    user.token = None
    user.save()


def verify_login(data):
    """A function that verifies if the login is done with the correct credentials."""
    session_id = auth.get_session_id(request)
    if session_id is not None and auth.check_session(session_id):
        abort(403, "user already logged in")
    if "email" not in data or "password" not in data:
        abort(400)
    email = data["email"]
    password = data["password"]
    user = auth.check_email(email)
    if user is None:
        abort(403, "email not found please sign up")
    if not user.check_password(base64.b64encode(password.encode("utf-8"))):
        abort(403, "password is incorrect")
    if not user.valid:
        abort(403, "email is not yet validated")
    session_id = auth.create_session(user.id)
    if session_id is None:
        abort(403, "there has been error while creating the session")
    return session_id


def verify_logout(request):
    """A function that verifies the logout."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    session = auth.get_session(session_id)
    auth.delete_session(session)


def get_profile(request):
    """A function that gets the user's profile information."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    session = auth.get_session(session_id)
    data = dict(filter(lambda x: x[0] != "token", session.user.to_dict().items()))
    if session.user.admin_account != []:
        data["admin"] = True
    if session.user.appointments != []:
        data["appointments"] = list(map(lambda x: x.to_dict() , session.user.appointments))
    return data


def get_profile_by_id(id):
    """A function that gets the user's profile information by id."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    user = storage.session.query(User).filter_by(id=id).first()
    if user:
        return dict(filter(lambda x: x[0] != "token", user.to_dict().items()))
    abort(403, "no user exists with this id")


def update_profile():
    """A function that updates the user's profile information."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    data = request.get_json()
    session = auth.get_session(session_id)
    user = session.user
    allowed = ["birth_date", "email", "first_name", "last_name", "location", "picture"]
    for key, val in data.items():
        if key in allowed:
            if key == "birth_date":
                if not isinstance(val, list) or len(val) != 3:
                    abort(403, "Birthdate should be in this format [Y, M, D]")
                setattr(user, key, datetime(*val))
                continue
            if key == "email":
                if not isinstance(val, str) or not re.search(
                    "^[\w_\-.0-9]+@\w+\.\w+$", val
                ):
                    abort(400, description=f"{val} is not valid")
            if key == "password":
                setattr(user, key, base64.b64encode(val.encode("utf-8")))
                continue
            setattr(user, key, val)
    user.save()
    return dict(filter(lambda x: x[0] != "token", session.user.to_dict().items()))


def delete_user():
    """A function that deletes a user."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    session = auth.get_session(session_id)
    storage.delete(session.user)
    storage.save()

def create_temp_password(email):
    if email is None:
        abort(400)
    user = auth.check_email(email)
    if user is None:
        abort(
            403,
            description="The provided email doesn't exists",
        )
    password = generate_password()
    tmp = TemporaryPassword(user_id=user.id, password=base64.b64encode(password.encode("utf-8")))
    tmp.save()
    send_password(user.first_name, user.email, password)
