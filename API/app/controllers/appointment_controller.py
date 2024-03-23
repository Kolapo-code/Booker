from flask import request, abort
from app import auth
from app import storage


def get_appointments():
    """A function that gets all the appointments for the admin."""
    user_by_session = auth.get_user_by_session_id(request)
    if not user_by_session:
        abort(403, "No session exists, try to log in.")
    if not user_by_session.admin_account:
        appointments = storage.get(cls="Appointment", user_id=user_by_session.id)
        if appointments == []:
            abort(404, "You have not done any appointments.")
    else:
        appointments = storage.get(cls="Appointment")
    return appointments


def get_appointment(appointment_id):
    """A function that gets the appointment with the given id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    appointment = storage.get(cls="Appointment", id=appointment_id)
    if not appointment:
        abort(404, "Appointment couldn't be found.")
    appointment_key = f"Appointment.{appointment_id}"
    appointment_instance = appointment.get(appointment_key)
    if appointment_instance.user_id != user.id and not user.admin_account:
        abort(403, "Not allowed to access the appointement.")
    if not appointment_instance:
        abort(404, "Appointment instance not found in dictionary")
    return appointment_instance.to_dict()


def put_appointment(appointment_id, data):
    """A function that updates the appointment with the given id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    appointment = storage.get(cls="Appointment", id=appointment_id)
    if not appointment:
        abort(404, "Appointment couldn't be found.")
    appointment_key = f"Appointment.{appointment_id}"
    appointment_instance = appointment.get(appointment_key)
    if not appointment_instance:
        abort(404, "Appointment instance not found in dictionary")
    if appointment_instance.user_id != user.id and not user.admin_account:
        abort(403, "Not allowed to update the appointement.")
    administration = False
    if user.admin_account:
        administration = True
    if not data:
        abort(403, "No update data was given.")
    keys = [
        "attended",
        "created_at",
        "date",
        "id",
        "range",
        "status",
        "updated_at",
        "user_id",
        "verify",
    ]
    for key, val in data.items():
        if key not in keys:
            abort(404, f"{key} is not recognized as an attribute in the appointment.")
        if (key == "attended" or key == "verify") and not (val == False or val == True):
            abort(404, f"Incorrect value type for {key}.")
        if (
            key == "created_at"
            or key == "updated_at"
            or key == "user_id"
            or key == "verify"
            and not administration
        ):
            abort(404, f"Not allowed to modify {key}.")
        if key == "status" and val not in ["Pending", "Verified", "Canceled"]:
            abort(404, f"Incorrect value for {key}.")
        # remember to check if the key is setted to the given value already
        # remember to take the workspace into considerations when the model is added.
        setattr(appointment_instance, key, val)
    appointment_instance.save()
    return appointment_instance.to_dict()
