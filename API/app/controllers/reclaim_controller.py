from flask import request, abort
from app import auth
from app import storage
from app.utils.helper import velidate_fields
from app.models.reclaim import Reclaim


def get_reclaim():
    """A function that gets all the reclaims of the user."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    reclaims = storage.get(cls="Reclaim", reclaimer_id=user.id)
    if not reclaims:
        return {}
    reclaims = list(reclaims.values())[0].to_dict()
    return reclaims


def post_reclaim(data):
    """A function that makes a reclaim by the user on another user."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not data:
        abort(400, "No data was passed in the form.")
    fields = {
        "subject": [15, 200],
        "description": [100, 2000],
        "reclaimed_id": "",
    }
    error = velidate_fields(fields, data)
    if error:
        abort(400, error)
    if not all(isinstance(val, str) for val in data.values()):
        abort(400, "The data should be of type string.")
    if data["reclaimed_id"] == user.id:
        abort(401, "You can't reclaim yourself, you crazy!")
    reclaimed_user = storage.get(cls="User", id=data["reclaimed_id"])
    if not reclaimed_user:
        abort(403, "The user being reclaimed doesn't exist.")
    for key, val in data.items():
        if key in ["subject", "description"] and (
            len(val) < fields[key][0] or len(val) > fields[key][1]
        ):
            abort(
                400,
                f"The {key} should not contain less than {fields[key][0]} characters nor more that {fields[key][1]} characters",
            )
    data["reclaimer_id"] = user.id
    reclaim = Reclaim(**data)
    reclaim.save()
