from app.views import app_views
from app.controllers.appointment_controller import get_appointments
from flask import jsonify


@app_views.route("/appointments", methods=["GET"])
def appointments():
    """A route that the admin can use to get all the appointments."""
    appointments = get_appointments()
    appointments_list = []
    for key, val in appointments.items():
        appointment = {}
        appointment[key] = val.to_dict()
        appointments_list.append(appointment)
    return jsonify({"Appointments": appointments_list}), 200
