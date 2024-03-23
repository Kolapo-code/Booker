from flask import request, abort
from app import auth
from app import storage
from app.models.appointment import Appointment
from datetime import datetime


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


def post_appointment(workspace_id, data):
    """A function that creates an appointment with the workspace id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    workspace = storage.get(cls="Workspace", id=workspace_id)
    if not workspace:
        abort(404, "Workspace couldn't be found.")
    if not data:
        abort(403, "No update appointment data was given.")
    appointment_data = {
        "date": "",
        "range": None,
    }
    for key, val in data.items():
        if key not in appointment_data.keys():
            abort(404, f"{key} is not recognized as an attribute in the appointment.")
        if key == "date":
            try:
                appointment_data["date"] = datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                abort(404, "Date string is not in the correct format %Y-%m-%d.")
        appointment_data[key] = val
    appointment_data["user_id"] = user.id
    appointment_data["workspace_id"] = workspace_id
    appointment = Appointment(**appointment_data)
    appointment.save()
    return appointment.id


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
    if data == {"status": "Canceled"} and appointment_instance.verify:
        abort(
            404,
            "You can't cancel Appointment, it has been verified by the workspace owner. Contact the owner.",
        )
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
