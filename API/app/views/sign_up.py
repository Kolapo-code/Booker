from app.views import app_views
from app import auth
from flask import jsonify, request, abort
from app.controllers.user_controller import post_user, put_validation, create_temp_password


@app_views.route("/sign_up", methods=["POST"])
def sign_up():
    """A route that handles the signup."""
    sesson_id = auth.get_session_id(request)
    if sesson_id is not None and auth.check_session(sesson_id):
        abort(403, "please log out first")
    data = request.get_json()
    user_id = post_user(data)
    return jsonify({"status": "created", "data": {"user_id": user_id}}), 201


@app_views.route("/validation/<token>", methods=["PUT"])
def validation(token):
    """A route that handles the validation of the token."""
    if token == "":
        abort(400, description="Empty token.")
    users = auth.get_user_by_token(token)
    if users is None:
        abort(403, description="No user was found.")
    put_validation(users)
    return jsonify({"status": "OK", "message": "account has been validated"}), 200


@app_views.route("/reset_password", methods=["POST"])
def reset_password():
    sesson_id = auth.get_session_id(request)
    if sesson_id is not None and auth.check_session(sesson_id):
        abort(403, 'forbidden')
    email = request.get_json().get('email')
    create_temp_password(email)
    return jsonify({"status": "OK", "message": "check your email for the temporary password"}), 201
