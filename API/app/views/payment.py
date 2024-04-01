from app.views import app_views
from app.controllers.payment_controller import (
    post_payment,
    get_payments,
    get_payment,
    invoice_payment,
)
from flask import jsonify, request


@app_views.route("/payments", methods=["POST"])
def set_payment():
    """A route that sets a new payment."""
    data = request.get_json()
    post_payment(data)
    return jsonify({"message": "Payment is set successfully"}), 201

@app_views.route("/payments", methods=["GET"])
def payments():
    """A route that gets all the payments of a the user."""
    payments = get_payments()
    return jsonify({"data": payments}), 200

@app_views.route("/payments/<id>", methods=["GET"])
def payment(id):
    """A route that gets the payment of a the user by id."""
    payment = get_payment(id)
    return jsonify({"data": payment}), 200


@app_views.route("/payments/invoice", methods=["GET"])
def payment_invoice():
    """A route that creates the payment invoice and sends it by email."""
    invoice_payment()
    return jsonify({"message": "The invoice has been generated and send by email."}), 200
