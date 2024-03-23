from app.views import app_views
from flask import jsonify, request

from app.controllers.workspace_controller import (
    get_workspaces,
    get_workspace,
    make_workspace
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


@app_views.route("/workspaces", methods=["POST"])
def create_workspaces():
    """A route that create a workspace"""
    workspace_id = make_workspace()
    return jsonify({
        "message": "workspace has been created successfuly",
        "data": {"workspace_id": workspace_id}
        }), 200
