from app.views import app_views
from flask import request
from app.controllers.appointment_controller import (
    get_appointments,
    get_appointment,
    post_appointment,
    put_appointment,
)
from flask import jsonify


@app_views.route("/appointments", methods=["GET"])
def appointments():
    """A route that can be used to get all the appointments."""
    appointments = get_appointments()
    return jsonify({"Appointments": appointments}), 200


@app_views.route("/appointments/<id>", methods=["GET"])
def appointment(id):
    """A route that can be used to get the appintment by id."""
    appointment = get_appointment(id)
    return jsonify({"Appointment": appointment}), 200


@app_views.route("/appointments/<id>", methods=["POST"])
def create_appointment(id):
    """A route that can be used to create an appointment."""
    print("here")
    data = request.get_json()
    appointment = post_appointment(id, data)
    return (
        jsonify({"message": "Appointment created successfully", "data": appointment}),
        200,
    )


@app_views.route("/appointments/<id>", methods=["PUT"])
def update_appointment(id):
    """A route that can be used to update an appointment."""
    data = request.get_json()
    appointment = put_appointment(id, data)
    return (
        jsonify({"message": "Appointment updated successfully", "data": appointment}),
        200,
    )


@app_views.route("/appointments/<id>/cancel", methods=["PUT"])
def cancel_appointment(id):
    """A route that can be used to cancel an appointment."""
    data = {"status": "Canceled"}
    appointment = put_appointment(id, data)
    if not appointment:
        return (
            jsonify({"message": "Appointment to be canceled by the workspace owner."}),
            200,
        )
    return (
        jsonify(
            {
                "message": "Appointment marked as canceled successfully",
                "data": appointment,
            }
        ),
        200,
    )
