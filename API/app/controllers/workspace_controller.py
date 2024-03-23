from flask import abort, request
from uuid import uuid4
from app import auth, storage
from app.models.workspace import Workspace


def get_workspaces():
    """A function that gets all the existing workspaces in db."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    workspaces = storage.get("Workspaces")
    data = map(lambda x: x.to_dict(), workspaces.values())
    return data


def get_workspace(id):
    """A function that gets a workspace by the id."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    workspace = storage.get("Workspaces", id=id)
    if not workspace:
        abort(403, "no workspace exists with this id")
    data = map(lambda x: x.to_dict(), workspace.values())
    return data[0]
