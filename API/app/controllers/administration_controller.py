from flask import request, abort
from app import auth
from app import storage
from app.models.admin_account import AdminAccount

""" User Administration """


def get_users():
    """A function that returns the users."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
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
        abort(403, "Not allowed to have access.")
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
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
    admin = AdminAccount(user_id=user_id)
    admin.save()
    if not admin:
        abort(403, "There has been an error setting up the admin.")
    return admin.id


def get_admins():
    """A function that gets all the admins"""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
    users = storage.get(cls="User")
    data = list(
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
    return data


def get_premiums():
    """A function that gets all the premium users"""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
    users = storage.get(cls="User")
    data = list(
        map(
            lambda user: {
                **user.to_dict(),
                **(
                    {"premium_account": user.premium_account.to_dict()}
                    if user.premium_account
                    else {}
                ),
            },
            filter(lambda user: user.premium_account, users.values()),
        )
    )
    for premium in data:
        premium.pop("admin_account", None)
    return data


def delete_user(user_id):
    """A function that deletes a user by id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
    user = storage.get(cls="User", id=user_id)
    storage.delete(user)
    storage.save()


""" Appointment Administration """


def get_appointments():
    """A function that gets all the appointments."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
    appointments = storage.get(cls="Appointment")
    data = list(map(lambda appointment: appointment.to_dict(), appointments.values()))
    return data


def get_appointment(id):
    """A function that gets the appointment by id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(403, "Not allowed to have access.")
    appointment = storage.get(cls="Appointment", id=id)
    data = list(appointment.values())[0].to_dict()
    return data
