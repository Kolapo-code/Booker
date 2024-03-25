from flask import abort, request
from app import auth, storage
from app.models.workspace import Workspace


def get_user_workspace_object(id):
    """
    gets a workspace object by the given
    id only if owned by the user
    """
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    user = auth.get_user_by_session_id(request)
    if user is None or not user.premium_account:
        abort(403, "no access please upgrade your account")
    if not user.premium_account.workspaces:
        abort(403, "you have no workspace")
    workspaces = list(filter(lambda x: x.id == id, user.premium_account.workspaces))
    if not workspaces:
        abort(403, "no workspace exists with this id")
    workspace = workspaces[0]
    return workspace


def get_workspaces():
    """A function that gets all the existing workspaces in db."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    workspaces = storage.get("Workspace")
    data = list(
        map(
            lambda x: dict(
                filter(
                    lambda d: d[0] != 'premium_account_id',x.to_dict().items()
                    )
                ), workspaces.values()
            )
        )
    return data


def get_workspace(id):
    """A function that gets a workspace by the id."""
    session_id = auth.get_session_id(request)
    if not session_id or not auth.check_session(session_id):
        abort(403, "no session exists, please log in")
    user = auth.get_user_by_session_id(request)
    workspaces = storage.get("Workspace", id=id)
    if not workspaces:
        abort(403, "no workspace exists with this id")
    workspace = list(workspaces.values())[0]
    data = dict(filter(lambda x: x[0] != 'premium_account_id', workspace.to_dict().items()))
    data["user_id"] = workspace.premium_account.user_id
    data["reviews"] = list(
        map(
            lambda x: dict(x.to_dict(), **{"likes": len(x.liked_users),
                                           "dislikes": len(x.disliked_users)}),
            workspace.reviews
            )
        )
    if user.premium_account and\
        user.premium_account.id == workspace.premium_account_id:
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
    if user.premium_account.workspaces:
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
    if len(data.keys()) != len(requirements.keys()):
        abort(400, 'bad request')
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


def update_workspace(id):
    """
    this function updates workspace by
    the data given in the request
    """
    workspace = get_user_workspace_object(id)
    requirements = {
        "title": (str, 60, 3),
        "field": (str, 60, 3),
        "description": (str, 500, 150),
        "picture": (str, 256, 0),
        "schedules": (str, 256, 0),
        "location": (str, 256, 30),
        "contact": (str, 256, 5)
    }
    """getting data from the request"""
    data = request.get_json()
    error = []
    list(map(lambda x: error.append(x[0])\
        if x[0] not in requirements or not isinstance(x[1], requirements[x[0]][0]) or\
            not (requirements[x[0]][2] <= len(x[1]) < requirements[x[0]][1])\
            else x, data.items()))
    if error:
        abort(400, f'some field not set correctly : {", ".join(error)}')
    for key, val in data.items():
        setattr(workspace, key, val)
    workspace.save()
    updated_data = dict(filter(lambda x: x[0] != 'premium_account_id', workspace.to_dict().items()))
    updated_data["user_id"] = workspace.premium_account.user_id
    return updated_data


def delete_workspace(id):
    """
    A function that cancels a
    workspace appointment by its id.
    """
    workspace = get_user_workspace_object(id)
    storage.delete(workspace)
    storage.save()


def get_workspace_appointments(id):
    """
    A function that gets a workspace
    appointments by the id.
    """
    workspace = get_user_workspace_object(id)
    data = list(map(lambda x: x.to_dict(), workspace.appointments))
    return data


def get_appointment_obj(workspace_id, appointment_id):
    """
    returns appointment object
    """
    workspace = get_user_workspace_object(workspace_id)
    appointment_list = list(filter(lambda x: x.id == appointment_id, workspace.appointments))
    if not appointment_list:
        abort(403, "this workspace doesn't have this appointment")
    appointment = appointment_list[0]
    return appointment


def get_workspace_appointment(id, appointment_id):
    """
    A function that gets a
    workspace appointment by its id.
    """
    appointment = get_appointment_obj(id, appointment_id)
    return appointment.to_dict()


def verify_workspace_appointment(id, appointment_id):
    """
    A function that verifies a
    workspace appointment by its id.
    """
    appointment = get_appointment_obj(id, appointment_id)
    appointment.status = "Verified"
    appointment.save()
    return appointment.to_dict()


def attended_workspace_appointment(id, appointment_id):
    """
    A function that attended a
    workspace appointment by its id.
    """
    appointment = get_appointment_obj(id, appointment_id)
    appointment.status = "Attended"
    appointment.save()
    return appointment.to_dict()


def cancel_workspace_appointment(id, appointment_id):
    """
    A function that cancels a
    workspace appointment by its id.
    """
    appointment = get_appointment_obj(id, appointment_id)
    if not appointment.to_be_canceled:
        abort(403, "this appoinment")
    appointment.status = "Canceled"
    appointment.save()
    return appointment.to_dict()
