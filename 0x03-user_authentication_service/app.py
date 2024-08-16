#!/usr/bin/env python3
""" Contains the flask app instance """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
