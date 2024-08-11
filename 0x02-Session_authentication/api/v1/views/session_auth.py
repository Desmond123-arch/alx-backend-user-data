#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """ Hanldes the user login """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    if len(User.search({'email': email})) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = User.search({'email': email})[0]
    if not user.is_valid_password(pwd=password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        data = jsonify(user.to_json())
        cookie_name = os.getenv('SESSION_NAME', )
        data.set_cookie(cookie_name, session_id)
        return data


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logouts the user"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
