from app.views import app_views
from flask import jsonify, request
from app.controllers.review_controller import post_review

@app_views.route("/workspaces/id/reviews", methods=["POST"])
def make_workspace_review(id):
    """A route that gets all the existing workspaces."""
    review_id = post_review(id)
    return jsonify({"data": {"reveiw_id": review_id}}), 201
