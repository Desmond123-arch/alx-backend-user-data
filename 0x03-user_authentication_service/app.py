#!/usr/bin/env python3
""" Contains the flask app instance """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """ Flask route for home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register():
    """ Registers a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return {"email": f"{email}", "message": "user created"}, 200


@app.route("/sessions", methods=["POST"])
def login():
    """ Logins a user in"""
    email = request.form.get("email")
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        result = jsonify({"email": f"{email}", "message": "logged in"})
        result.set_cookie('session_id', session_id)
        return result, 200
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """ Logouts a user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/', code=302)


@app.route("/profile", methods=["GET"])
def profile():
    """ Creates a profile for a user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """ Gets the reset token endpoint"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """ Resets the users password """
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')
    try:
        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
