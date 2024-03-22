from flask import request, abort
from app import auth
from app import storage
from app.models.admin_account import AdminAccount


def post_admin(user_id):
    """A function that sets up a user to be an admin."""
    user_by_session = auth.get_user_by_session_id(request)
    if not user_by_session:
        abort(403, "No session exists, try to log in.")
    admin = storage.get(cls="AdminAccount", user_id=user_by_session.id)
    if admin == {}:
        abort(403, "Not allowed to setup a new admin.")
    admin = AdminAccount(user_id=user_id)
    admin.save()
    if not admin:
        abort(403, "There has been an error setting up the admin.")
    return admin.id
