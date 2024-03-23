from flask import abort, request
from uuid import uuid4
from app import auth, storage
from app.models.workspace import Workspace


def get_workspaces():
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    workspaces = storage.get("Workspaces")
    data = map(lambda x : x.to_dict(), workspaces.values())
    return data


def get_workspace(id):
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    workspace = storage.get("Workspaces", id=id)
    if not workspace:
        abort(403, "no workspace exists with this id")
    data = map(lambda x : x.to_dict(), workspace.values())
    return data[0]


def make_workspace():
    """
    this function makes workspace by
    the data given in the request
    """
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    user = auth.get_user_by_session_id(session_id)
    if user is None or not user.premium_account:
        abort(403, "no access please upgrade your account")
    if user.premium_account.workspaces:
        abort(403, "your are only allowed to create one workspace")
    requirements = {
        "title": (str, 60, 3),
        "feild": (str, 60, 3),
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
    data["premium_account_id"] = user.premium_account.id
    workspace = Workspace(**data)
    workspace.save()
    return workspace.id
