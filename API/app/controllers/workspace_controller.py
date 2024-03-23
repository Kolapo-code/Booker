from flask import abort, request
from uuid import uuid4
from app import auth, storage
from app.models.workspace import Workspace


def get_workspaces():
    """A function that gets all the existing workspaces in db."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    workspaces = storage.get("Workspace")
    data = list(map(lambda x: x.to_dict(), workspaces.values()))
    return data


def get_workspace(id):
    """A function that gets a workspace by the id."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    user = auth.get_user_by_session_id(request)
    workspace_list = storage.get("Workspace", id=id)
    if not workspace_list:
        abort(403, "no workspace exists with this id")
    workspace = list(workspace_list.values())[0]
    data = workspace.to_dict()
    if user.premium_account and\
        user.premium_account[0].id == workspace.premium_account_id:
        data["appointments"] = list(map(lambda x: x.to_dict(), workspace.appointments))
    return data


def make_workspace():
    """
    this function makes workspace by
    the data given in the request
    """
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    user = auth.get_user_by_session_id(request)
    if user is None or not user.premium_account:
        abort(403, "no access please upgrade your account")
    if user.premium_account[0].workspaces:
        abort(403, "your are only allowed to create one workspace")
    requirements = {
        "title": (str, 60, 3),
        "field": (str, 60, 3),
        "description": (str, 500, 150),
        "picture": (str, 256, 0),
        "schedules": (str, 256, 0),
        "location": (str, 256, 30),
        "contact": (str, 256, 5)
    }
    data = request.get_json()
    error = []
    list(map(lambda x: error.append(x[0])\
        if x[0] not in requirements or not isinstance(x[1], requirements[x[0]][0]) or\
            not (requirements[x[0]][2] <= len(x[1]) < requirements[x[0]][1])\
            else x, data.items()))
    if error:
        abort(400, f'some field not set correctly : {", ".join(error)}')
    data["premium_account_id"] = user.premium_account[0].id
    workspace = Workspace(**data)
    workspace.save()
    return workspace.id
