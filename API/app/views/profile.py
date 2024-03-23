from app.views import app_views
from flask import jsonify, request
from app.controllers.user_controller import (
    get_profile,
    get_profile_by_id,
    update_profile,
    delete_user,
    upgrade_to_premium,
)


@app_views.route("/profile", methods=["GET"])
def my_profile():
    """A route that gets the user's profile information"""
    user_data = get_profile(request)
    return jsonify({"data": user_data}), 200


@app_views.route("/profile/<id>", methods=["GET"])
def profile(id):
    """A route that gets the user's profile information by the id."""
    user_data = get_profile_by_id(id)
    return jsonify({"data": user_data}), 200


@app_views.route("/profile", methods=["PUT"])
def manage_profile():
    """A route that updates the user's profile information"""
    user_data = update_profile()
    return jsonify({"message": "profile has been updated successfully",
                    "data": user_data}), 200


@app_views.route("/account", methods=["DELETE"])
def delete_account():
    """A route that deletes the user's account."""
    delete_user()
    return jsonify({"message": "account has been deleted"}), 200


@app_views.route("/account/upgrade", methods=["POST"])
def upgrade_account():
    """A route that upgrades the user's account."""
    upgrade_to_premium()
    return jsonify({"message": "Account has been upgraded to premium."}), 200
