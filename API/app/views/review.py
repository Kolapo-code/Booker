from app.views import app_views
from flask import jsonify, request
from app.controllers.review_controller import (
    post_review,
    like_review,
    dislike_review,
    update_review,
    delete_review
    )

@app_views.route("/workspaces/id/reviews", methods=["POST"])
def make_workspace_review(id):
    """A route that makes a review."""
    review_id = post_review(id)
    return jsonify({"data": {"reveiw_id": review_id}}), 201


@app_views.route("/reviews/id", methods=["PUT"])
def edit_review(id):
    """A route that updates a review."""
    review_data = update_review(id)
    return jsonify({"data": review_data, "message": "review has been updated"}), 200


@app_views.route("/reviews/id", methods=["DELETE"])
def remove_review(id):
    """A route that deletes a review."""
    delete_review(id)
    return jsonify({"data": [], "message": "review has been deleted"}), 200


@app_views.route("/reviews/id/like", methods=["POST"])
def like_workspace_review(id):
    """A route that gets all the existing workspaces."""
    likes_num = like_review(id)
    return jsonify({"data": {"likes": likes_num}}), 201


@app_views.route("/reviews/id/dislike", methods=["POST"])
def dislike_workspace_review(id):
    """A route that gets all the existing workspaces."""
    dislikes_num = dislike_review(id)
    return jsonify({"data": {"likes": dislikes_num}}), 201
