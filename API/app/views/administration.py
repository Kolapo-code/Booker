from app.views import app_views
from flask import jsonify, abort
from app.controllers.administration_controller import (
    get_users,
    ban_unban_user,
    post_admin,
    get_admins,
    get_premiums,
    delete_user,
    get_appointments,
    get_appointment,
)

""" User Administration """


@app_views.route("/admin/user", methods=["GET"])
def admin_users():
    """A route that the admin can use to get all the users."""
    users = get_users()
    users_list = []
    for val in users.values():
        user = val.to_dict()
        user.pop("admin_account", None)
        users_list.append(user)
    return jsonify({"data": users_list}), 201


@app_views.route("/admin/user/<user_id>/ban", methods=["PUT"])
def admin_user_ban(user_id):
    """A route that the admin can use to ban a user."""
    ban_unban_user(user_id, True)
    return jsonify({"message": f"The user with id: {user_id} has been banned."}), 201


@app_views.route("/admin/user/<user_id>/unban", methods=["PUT"])
def admin_user_unban(user_id):
    """A route that the admin can use to unban a user."""
    ban_unban_user(user_id, False)
    return jsonify({"message": f"The user with id: {user_id} has been unbanned."}), 201


@app_views.route("/admin/user/<user_id>/setup_admin", methods=["POST"])
def admin_setup_admin(user_id):
    """A route that the admin can use to set up a user for the admin role."""
    if user_id == "":
        abort(400, "Empty user id.")
    admin_id = post_admin(user_id)
    return jsonify({"status": "admin created", "admin_id": admin_id}), 201


@app_views.route("/admin/user/admins", methods=["GET"])
def admin_admins():
    """A route that the admin can use to get all the admin users."""
    admins = get_admins()
    return jsonify({"data": admins}), 201


@app_views.route("/admin/user/premiums", methods=["GET"])
def admin_premiums():
    """A route that the admin can use to get all the premium users."""
    premiums = get_premiums()
    return jsonify({"data": premiums}), 201


@app_views.route("/admin/user/<user_id>/delete", methods=["GET"])
def admin_delete_user(user_id):
    """A route that the admin can use to get all the premium users."""
    delete_user()
    return jsonify({"message": f"{user_id} is deleted successfully"}), 201


""" Appointment Administration """


@app_views.route("/admin/appointment", methods=["GET"])
def admin_appointments():
    """A route that the admin can use to get all the appointments."""
    appointments = get_appointments()
    return jsonify({"Appointments": appointments}), 200


@app_views.route("/admin/appointment/<id>", methods=["GET"])
def admin_appointment(id):
    """A route that the admin can use to get the appintment by id."""
    appointment = get_appointment(id)
    return jsonify({"Appointment": appointment}), 200
