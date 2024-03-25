from flask import request, abort
from app import auth
from app import storage
from app.models.review import Review


def post_review(workspace_id):
    """A function that creates an appointment with the workspace id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    workspace = storage.get("Workspace", id=workspace_id)
    if not workspace:
       abort(404, "Workspace couldn't be found.")
    requirements = {
        "title": (str, 60, 3),
        "content": (str, 1500, 10),
    }
    data = request.get_json()
    error = []
    list(map(lambda x: error.append(x[0])\
        if x[0] not in requirements or not isinstance(x[1], requirements[x[0]][0]) or\
            not (requirements[x[0]][2] <= len(x[1]) < requirements[x[0]][1])\
            else x, data.items()))
    if error:
        abort(400, f'Some field are not set correctly : {", ".join(error)}')
    data["reviewer_id"] = user.id
    data["workspace_id"] = workspace_id
    review = Review(**data)
    review.save()
    return review.id
