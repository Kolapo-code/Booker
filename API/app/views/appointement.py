from app.views import app_views
from flask import jsonify
from app.controllers.appointment_controller import get_appointments


@app_views.route("/appointments", methods=["GET"])
def appointments():
    appointments = get_appointments()
    return jsonify({ "Appointments": appointments}), 200
