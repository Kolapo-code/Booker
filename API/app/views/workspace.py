from app.views import app_views
from flask import jsonify, request

from app.controllers.workspace_controller import (
    get_workspaces,
    get_workspace,
    make_workspace,
    update_workspace,
    get_workspace_appointments,
    get_workspace_appointment,
    verify_workspace_appointment,
    attended_workspace_appointment,
    cancel_workspace_appointment,
    delete_workspace
)


@app_views.route("/workspaces", methods=["GET"])
def workspaces():
    """A route that gets all the existing workspaces."""
    workspaces_data = get_workspaces()
    return jsonify({"data": workspaces_data}), 200


@app_views.route("/workspaces/<id>", methods=["GET"])
def workspace(id):
    """A route that gets a workspace by the id."""
    workspace_data = get_workspace(id)
    return jsonify({"data": workspace_data}), 200


@app_views.route("/workspaces/<id>/appointments", methods=["GET"])
def workspace_appointments(id):
    """A route that gets all the workspace appointments."""
    appointments_data = get_workspace_appointments(id)
    return jsonify({"data": appointments_data}), 200


@app_views.route("/workspaces/<id>/appointments/<appointment_id>", methods=["GET"])
def workspace_appointment(id, appointment_id):
    """A route that gets a workspace appointments by the id."""
    appointment_data = get_workspace_appointment(id, appointment_id)
    return jsonify({"data": appointment_data}), 200


@app_views.route("/workspaces", methods=["POST"])
def create_workspaces():
    """A route that create a workspace"""
    workspace_id = make_workspace()
    return jsonify({
        "message": "workspace has been created successfuly",
        "data": {"workspace_id": workspace_id}
        }), 201

@app_views.route("/workspaces/<id>", methods=["PUT"])
def modify_workspaces(id):
    """A route that create a workspace"""
    updated_data = update_workspace(id)
    return jsonify({
        "message": "workspace has been updated successfuly",
        "data": updated_data
        }), 200


@app_views.route("/workspaces/<id>/appointments/<appointment_id>/verify", methods=["PUT"])
def verify_appointment(id, appointment_id):
    """A route that verifies a workspace appointments by the id."""
    appointment_data = verify_workspace_appointment(id, appointment_id)
    return jsonify({
        "message": "appointment has been verified successfuly",
        "data": appointment_data
        }), 200


@app_views.route("/workspaces/<id>/appointments/<appointment_id>/attended", methods=["PUT"])
def attended_appointment(id, appointment_id):
    """A route that attends a workspace appointments by the id."""
    appointment_data = attended_workspace_appointment(id, appointment_id)
    return jsonify({
        "message": "appointment has been made attended successfuly",
        "data": appointment_data
        }), 200


@app_views.route("/workspaces/<id>/appointments/<appointment_id>/cancel", methods=["PUT"])
def cancel_appointment_by_workspace(id, appointment_id):
    """A route that cancels a workspace appointments by the id."""
    appointment_data = cancel_workspace_appointment(id, appointment_id)
    return jsonify({
        "message": "appointment has been canceled successfuly",
        "data": appointment_data
        }), 200


@app_views.route("/workspaces/<id>", methods=["DELETE"])
def remove_workspace(id):
    """A route that deletes a workspace appointments by the id."""
    delete_workspace(id)
    return jsonify({
        "message": "appointment has been deleted successfuly",
        "data": []
        }), 200
