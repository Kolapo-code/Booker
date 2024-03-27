from app.views import app_views
from flask import jsonify, request
from app.controllers.reclaim_controller import (
    post_reclaim,
    get_reclaim,
)


@app_views.route("/reclaim", methods=["GET"])
def reclaims():
    """A route that lists all the reclaims done by the user."""
    data = get_reclaim()
    return (
        jsonify({"data": data}),
        202,
    )


@app_views.route("/reclaim", methods=["POST"])
def make_reclaim():
    """A route that a user can use to make a reclaim."""
    data = request.get_json()
    post_reclaim(data)
    return (
        jsonify({"message": f"You reclaim will be resolved by the administration."}),
        201,
    )
