from flask import request, abort
from app import auth
from app import storage


def get_appointments():
    """A function that gets all the appointments for the admin."""
    user_by_session = auth.get_user_by_session_id(request)
    if not user_by_session:
        abort(403, "No session exists, try to log in.")
    admin = storage.get(cls="AdminAccount", user_id=user_by_session.id)
    if admin == {}:
        abort(403, "Not allowed to access appointements")
    appointments = storage.get(cls="Appointment")
    return appointments
