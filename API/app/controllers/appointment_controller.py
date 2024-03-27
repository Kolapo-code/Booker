from flask import request, abort
from app import auth
from app import storage
from app.models.appointment import Appointment
from datetime import datetime


def get_appointments():
    """A function that gets all the appointments for the admin."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    appointments = storage.get(cls="Appointment", user_id=user.id)
    data = list(map(lambda appointment: appointment.to_dict(), appointments.values()))
    return data


def get_appointment(appointment_id):
    """A function that gets the appointment with the given id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    appointment = storage.get(cls="Appointment", id=appointment_id)
    if not appointment:
        abort(404, "Appointment couldn't be found.")
    appointment = list(appointment.values())[0]
    if appointment.user_id != user.id:
        abort(404, "The appointment doesn't exist.")
    data = appointment.to_dict()
    return data


def post_appointment(workspace_id, data):
    """A function that creates an appointment with the workspace id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    workspace = storage.get(cls="Workspace", id=workspace_id)
    if not workspace:
        abort(404, "Workspace couldn't be found.")
    if not data:
        abort(400, "No update appointment data was given.")
    appointment_data = {
        "date": "",
        "range": None,
    }
    for key, val in data.items():
        if key not in appointment_data.keys():
            abort(400, f"{key} is not recognized as an attribute in the appointment.")
        if key == "date":
            try:
                appointment_data["date"] = datetime.strptime(val, "%Y-%m-%d")
            except (ValueError, TypeError):
                abort(400, "Date string is not in the correct format %Y-%m-%d.")
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
    if appointment_instance.status in ["Canceled", "Verified"]:
        abort(401, "This appointment is canceled and can't be modified.")
    if data == {"status": "Canceled"} and appointment_instance.status == "Verified":
        appointment_instance.to_be_canceled = True
        appointment_instance.save()
        return {}
    if appointment_instance.user_id != user.id and not user.admin_account:
        abort(401, "Not allowed to update the appointement.")
    if not data:
        abort(400, "No update data was given.")
    keys = [
        "date",
        "range",
        "status",
    ]
    for key, val in data.items():
        if key not in keys:
            abort(400, f"{key} is not recognized as an attribute in the appointment.")
        if key == "status" and val not in ["Pending", "Canceled"]:
            abort(400, f"Incorrect value for {key}.")
        if key == "status" and val in ["Verified", "Attended"]:
            abort(401, "You are not allowed to modify the field.")
        setattr(appointment_instance, key, val)
    appointment_instance.save()
    return appointment_instance.to_dict()
