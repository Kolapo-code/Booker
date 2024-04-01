from flask import request, abort
from app import auth
from app import storage
from datetime import datetime
from app.models.payment import Payment
from app.utils.helper import validate_fields


def post_payment(data):
    """A function that sets a new payment."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.premium_account:
        abort(403, "You have to set the upgrade your account to do this procedure.")
    fields = {
        "amount": None,
        "card_type": "",
        "card_owner": "",
        "card_number": "",
        "card_cvv": "",
        "card_expiry_date": "",
    }
    error_string = validate_fields(fields, data)
    if error_string != "":
        abort(403, error_string)
    date = None
    for key, val in data.items():
        if key == "amount" and not isinstance(val, int):
            abort(400, "The amount should be of type integer.")
        if key == "card_type" and val not in ["Visa", "Master Card"]:
            abort(
                400, "Make sure you set the card type correctly: [Visa, Master Card]."
            )
        if key == "card_owner" and len(val) > 100:
            abort(400, "Make sure the card_owner contains your legal name.")
        if key == "card_number" and not len(val) == 16:
            abort(400, "Make sure you give a valid card number.")
        if key == "card_cvv" and len(val) != 3:
            abort(400, "Make sure the card_cvv is correct.")
        if key == "card_expiry_date":
            try:
                date = datetime.strptime(val + "-01", "%Y-%m-%d").date()
                print(date)
            except (TypeError, ValueError):
                abort(400, "Date string is not in the correct format %Y-%m.")
            if date < date.today():
                abort(400, "You card is expired.")
    data["card_expiry_date"] = date
    data["premium_account_id"] = user.premium_account.id
    payment = Payment(**data)
    payment.save()


def get_payments():
    """A function that gets the payments of the session user."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.premium_account:
        abort(403, "You have to set the upgrade your account to do this procedure.")
    payments = storage.get(cls="Payment", premium_account_id=user.premium_account.id)
    data = list(
        map(
            lambda payment: dict(
                filter(
                    lambda d: d[0] != "premium_account_id", payment.to_dict().items()
                )
            ),
            payments.values(),
        )
    )
    return data


def get_payment(id):
    """A function that gets the payments of the session user by id."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.premium_account:
        abort(403, "You have to set the upgrade your account to do this procedure.")
    payment = storage.get(
        cls="Payment", id=id, premium_account_id=user.premium_account.id
    )
    if not payment:
        abort(403, "There is no payment with the given id.")
    data = list(payment.values())[0].to_dict()
    data.pop("premium_account_id")
    return data


def invoice_payment():
    """A function that gets the payments of the session user and creates an invoice
    and sends it to the user's email."""
    user = auth.get_user_by_session_id(request)
    if not user:
        abort(403, "No session exists, try to log in.")
    if not user.premium_account:
        abort(403, "You have to set the upgrade your account to do this procedure.")
    payments = storage.get(cls="Payment", premium_account_id=user.premium_account.id)
    data = list(map(lambda payment: payment.to_dict(), payments.values()))
    payment = Payment()
    payment.generate_invoice(data, user.first_name, user.last_name, user.email)
    return data
