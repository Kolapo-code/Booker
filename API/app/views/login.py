from app.views import app_views
from flask import jsonify, request, abort, make_response
from app.controllers.user_controller import verify_login, verify_logout


@app_views.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session_id = verify_login(data)
    responce = make_response({"email": data['email'], "message": "logged in"})
    responce.set_cookie("session_id", session_id)
    return responce

@app_views.route("/logout", methods=["DELETE"])
def logout():
    verify_logout(request)
    responce = make_response({"message": "logged out"})
    responce.set_cookie("session_id", "", expires=0)
    return responce
