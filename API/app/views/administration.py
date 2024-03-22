from app.views import app_views
from app.controllers.administration_controller import post_admin
from flask import jsonify, abort


@app_views.route("/setup_admin/<user_id>", methods=["POST"])
def setup_admin(user_id):
    """A route that the admin can use to set up a user for the admin role."""
    if user_id == "":
        abort(400, "Empty user id.")
    admin_id = post_admin(user_id)
    return jsonify({"status": "admin created", "admin_id": admin_id}), 201
