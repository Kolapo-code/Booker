from app.views import app_views
from flask import jsonify, request, abort, make_response
from app.controllers.user_controller import get_profile, get_profile_by_id, update_profile, delete_user


@app_views.route("/profile", methods=["GET"])
def my_profile():
    """get user profile information"""
    user_data = get_profile(request)
    return jsonify({"data": user_data}), 200


@app_views.route("/profile/<id>", methods=["GET"])
def profile(id):
    """get user profile information"""
    user_data = get_profile_by_id(id)
    return jsonify({"data": user_data}), 200


@app_views.route("/profile", methods=["PUT"])
def manage_profile():
    """update user profile information"""
    user_data = update_profile()
    return jsonify({"data": user_data}), 200


@app_views.route("/account", methods=["DELETE"])
def delete_account():
    """delete user"""
    delete_user()
    return jsonify({"message": "account has been deleted"}), 200
