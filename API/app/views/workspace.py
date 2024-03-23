from app.views import app_views
from flask import jsonify, request
from app.controllers.workspace_controller import (
    get_workspaces,
    get_workspace
)



@app_views.route("/workspaces", methods=["GET"])
def all_workspaces():
    """A route that gets the user's profile information"""
    workspaces_data = get_workspaces()
    return jsonify({"data": workspaces_data}), 200


@app_views.route("/workspaces/id", methods=["GET"])
def all_workspaces(id):
    """A route that gets the user's profile information"""
    workspace_data = get_workspace(id)
    return jsonify({"data": workspace_data}), 200
