from app.models.temporary_password import TemporaryPassword
from app.utils.helper_ import send_password, generate_password
from app.models.premium_account import PremiumAccount
from app.utils.helper import verify_email
from datetime import datetime, timedelta
from flask import abort, request
from app.models.user import User
from app import auth, storage
from uuid import uuid4
import base64
import re


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
    if session.user.appointment != []:
        data["appointments"] = list(
            map(lambda x: x.to_dict(), session.user.appointment)
        )
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
    tmp = TemporaryPassword(
        user_id=user.id, password=base64.b64encode(password.encode("utf-8"))
    )
    tmp.save()
    send_password(user.first_name, user.email, password)


def upgrade_to_premium():
    """A function that upgrades the account to premium."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "no session exists, please log in")
    data = request.get_json()
    premium_account = {
        "field": "",
        "location": "",
        "biography": "",
        "subscription_plan": "",
        "auto_renewal": "",
    }
    for key, val in data.items():
        if key not in premium_account.keys():
            abort(403, f"{key} no existent in the upgrade form.")
        if key in ["field", "location", "biography"] and val is None:
            abort(403, f"{key} must have a value.")
        if key == "subscription_plan" and val not in ["Montly", "Yearly"]:
            abort(403, f"{key} must be eather [Montly] or [Yearly].")
        if key == "auto_renewal" and not (val == False or val == True):
            abort(403, f"{key} must be eather [True] or [False].")
        # FIND A WAY TO APPLY SOME CRITERIA ON THE LOCATION FIELD.
        if key == "biography":
            if len(val) < 150:
                abort(403, f"{key} must be at least 150 characters.")
            if len(val) > 300:
                abort(403, f"{key} must be at most 300 characters.")
        premium_account[key] = val
    premium_account["user_id"] = user.id
    premium_account["subscription_start_date"] = datetime.now()
    if data.get("subscription_plan") == "Montly":
        premium_account["subscription_end_date"] = datetime.now() + timedelta(days=30)
    else:
        premium_account["subscription_end_date"] = datetime.now() + timedelta(days=365)
    premium_instance = PremiumAccount()
    for key, val in premium_account.items():
        setattr(premium_instance, key, val)
    premium_instance.save()
