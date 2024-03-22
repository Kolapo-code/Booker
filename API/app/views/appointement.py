from app.views import app_views
from flask import request
from app.controllers.appointment_controller import (
    get_appointments,
    get_appointment,
    put_appointment,
)
from flask import jsonify


@app_views.route("/appointments", methods=["GET"])
def appointments():
    """A route that can be used to get all the appointments."""
    appointments = get_appointments()
    appointments_list = []
    for key, val in appointments.items():
        appointment = {}
        appointment[key] = val.to_dict()
        appointments_list.append(appointment)
    return jsonify({"Appointments": appointments_list}), 200


@app_views.route("/appointments/<id>", methods=["GET"])
def appointment(id):
    """A route that can be used to get the appintment by id."""
    appointment = get_appointment(id)
    return jsonify({"Appointment": appointment}), 200


@app_views.route("/appointments/<id>", methods=["PUT"])
def update_appointment(id):
    """A route that can be used to update an appointment."""
    data = request.get_json()
    appointment = put_appointment(id, data)
    return jsonify({"Appointment updated successfully": appointment}), 200

@app_views.route("/appointments/<id>/cancel", methods=["PUT"])
def cancel_appointment(id):
    """A route that can be used to cancel an appointment."""
    data = {"status": "Canceled"}
    appointment = put_appointment(id, data)
    return jsonify({"Appointment updated successfully": appointment}), 200
