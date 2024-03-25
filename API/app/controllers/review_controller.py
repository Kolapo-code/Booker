from flask import request, abort
from app import auth
from app import storage
from app.models.review import Review


def post_review(workspace_id):
    """A function that creates an review with the workspace id."""
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
    if len(data.keys()) != len(requirements.keys()):
        abort(400, 'bad request')
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


def update_review(id):
    """A function that updates an review."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    review = list(filter(lambda x: x.id == id, user.reviews))
    if not review:
        abort(404, "Review couldn't be found.")
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
    for key, val in data.items():
        setattr(review, key, val)
    review.save()
    return review.to_dict()


def delete_review(id):
    """A function that updates an review."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    review = list(filter(lambda x: x.id == id, user.reviews))
    if not review:
        abort(404, "Review couldn't be found.")
    storage.delete(review)
    storage.save()



def like_review(id):
    """A function that likes a review"""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    review = storage.get('Review', id=id)
    if not review:
        abort(404, "Review couldn't be found.")
    review = list(review.values())[0]
    if user not in review.liked_users:
        if user in review.desliked_users:
            review.desliked_users.remove(user)
        review.liked_users.append(user)
        review.save()
    return len(review.liked_users)


def dislike_review(id):
    """A function that dislikes a review"""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    review = storage.get('Review', id=id)
    if not review:
        abort(404, "Review couldn't be found.")
    review = list(review.values())[0]
    if user not in review.disliked_users:
        if user in review.liked_users:
            review.liked_users.remove(user)
        review.disliked_users.append(user)
        review.save()
    return len(review.disliked_users)
