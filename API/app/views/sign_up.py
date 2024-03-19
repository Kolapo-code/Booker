from app.views import app_views
from flask import jsonify, request, abort
from app import auth
from app.models.regular_user import RegularUser
from app import storage
from uuid import uuid4
from datetime import datetime
import base64

@app_views.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
        sesson_id = auth.get_session_id(request)
        if auth.check_session(sesson_id):
            """if session still exists"""
            abort(403)
        data_list = [
            "first_name",
            "last_name",
            "email",
            "password",
            "birth_date",
            "location",
        ]
        user_data = {}
        for key in data_list:
            if key not in data:
                return jsonify({'error': f'{key} does not exits in the given data'}), 400
            if key == "birth_date":
                if not isinstance(data[key], list) or len(data[key]) != 3:
                    return jsonify({'error': 'birth_date should be in this format [Y, M, D]'}), 400
                user_data[key] = datetime(*data[key])
                continue
            if key == "password":
                user_data[key] = base64.b64encode(data[key].encode('utf-8'))
                continue
            user_data[key] = data[key]
        token = str(uuid4())
        user_data['token'] = token
        user = RegularUser(**user_data)
        user.save()
        """call the function that sends email token"""
        return jsonify({'status': 'created', 'user_id': user.id}), 201
    except Exception:
        """if request is unvalid"""
        abort(400)


@app_views.route('/validation/<token>', methods=['PUT'])
def validation(token):
    if token == '':
        abort(400)
    users = storage.get('RegularUser', token=token)
    if users == {}:
        abort(403)
    user = list(users.values())[0]
    user.valid = True
    user.token = None
    user.save()
    return jsonify({'status': "OK"}), 200
