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
    redirect('/', code=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
