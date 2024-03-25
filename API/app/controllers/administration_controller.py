from flask import request, abort
from app import auth
from app import storage
from app.models.admin_account import AdminAccount


""" VERIFYING ADMINISTRATION RIGHTS"""


def verify_administration():
    """A function that verifies if the session user has administration rights."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.admin_account:
        abort(401, "Not allowed to have access.")


""" Users Administration """


def get_users():
    """A function that returns the users."""
    verify_administration()
    users = storage.get(cls="User")
    if not users:
        abort(404, "No users found.")
    return users


def ban_unban_user(user_id, order):
    """A function that bans or unbans a user."""
    verify_administration()
    user = storage.get(cls="User", id=user_id)
    if not user:
        abort(404, "No user found.")
    user = list(user.values())[0]
    if order:
        user.ban = True
    else:
        user.ban = False
    user.save()
    return user


def post_admin(user_id):
    """A function that sets up a user to be an admin."""
    verify_administration()
    admin = AdminAccount(user_id=user_id)
    admin.save()
    if not admin:
        abort(403, "There has been an error setting up the admin.")
    return admin.id


def get_admins():
    """A function that gets all the admins"""
    verify_administration()
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
    verify_administration()
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
    verify_administration()
    user = storage.get(cls="User", id=user_id)
    storage.delete(user)
    storage.save()


""" Appointments Administration """


def get_appointments():
    """A function that gets all the appointments."""
    verify_administration()
    appointments = storage.get(cls="Appointment")
    data = list(map(lambda appointment: appointment.to_dict(), appointments.values()))
    return data


def get_appointment(id):
    """A function that gets the appointment by id."""
    verify_administration()
    appointment = storage.get(cls="Appointment", id=id)
    data = list(appointment.values())[0].to_dict()
    return data


""" Reclaims Administration """


def get_reclaims():
    """A function that gets the all reclaims."""
    verify_administration()
    reclaims = storage.get(cls="Reclaims")
    data = list(map(lambda reclaim: reclaim.to_dict(), reclaims.values()))
    return data


def get_reclaim(reclaim_id):
    """A function that gets a reclaim by the id."""
    verify_administration()
    reclaim = storage.get(cls="Reclaims", id=reclaim_id)
    data = list(reclaim.values())[0].to_dict()
    return data


def get_reclaim(reclaim_id):
    """A function that gets a reclaim by the id."""
    verify_administration()
    reclaim = storage.get(cls="Reclaims", id=reclaim_id)
    data = list(reclaim.values())[0].to_dict()
    return data


def resolve_reclaim(reclaim_id):
    """A function that sets a reclaim as resolved."""
    verify_administration()
    reclaim = storage.get(cls="Reclaims", id=reclaim_id)
    # update the reclaim
    reclaim.status = "Resolved"
    reclaim.save()
    # Since its now resolved we shall send an email saying the problem has been resolved.
    data = list(reclaim.values())[0].to_dict()
    return data
