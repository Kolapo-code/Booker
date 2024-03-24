from flask import request, abort
from app import auth
from app import storage
from app.models.admin_account import AdminAccount


def get_users():
    """A function that returns the users."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to get the users.")
    users = storage.get(cls="User")
    if not users:
        abort(403, "No users found.")
    return users


def ban_unban_user(user_id, order):
    """A function that bans or unbans a user."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to ban the user.")
    user = storage.get(cls="User", id=user_id)
    if not user:
        abort(403, "No user found.")
    user = list(user.values())[0]
    if order:
        user.ban = True
    else:
        user.ban = False
    user.save()
    return user


def post_admin(user_id):
    """A function that sets up a user to be an admin."""
    user_by_session = auth.get_user_by_session_id(request)
    if not user_by_session:
        abort(403, "No session exists, try to log in.")
    if not user_by_session.admin_account:
        abort(403, "Not allowed to setup a new admin.")
    admin = AdminAccount(user_id=user_id)
    admin.save()
    if not admin:
        abort(403, "There has been an error setting up the admin.")
    return admin.id


def get_admins():
    """A function that gets all the admins"""
    user_by_session = auth.get_user_by_session_id(request)
    if not user_by_session:
        abort(403, "No session exists, try to log in.")
    if not user_by_session.admin_account:
        abort(403, "Not allowed to get the admins.")
    users = storage.get(cls="User")
    admins = list(
        map(
            lambda user: {
                **user.to_dict(),
                **(
                    {"admin_account": user.admin_account.to_dict()}
                    if user.admin_account
                    else {}
                ),
            },
            filter(lambda user: user.admin_account, users.values()),
        )
    )
    return admins
