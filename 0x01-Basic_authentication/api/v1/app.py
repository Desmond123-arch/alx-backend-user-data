#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
print("Blueprint registed")
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")

access_routes = ['/api/v1/status/',
                 '/api/v1/unauthorized/', '/api/v1/forbidden/']
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def b4_request() -> None:
    """ Called before each request"""
    if auth is None:
        return
    if not auth.require_auth(request.path, access_routes):
        return
    if auth.authorization_header(request) == None:
        abort(401)

    if auth.current_user(request) == None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """  Hanldles unauthorized requests """
    return jsonify({"error" : "Unauthorized"}), 401


@app.errorhandler(403)
def forbbiden(error) -> str:
    """ Forbidden handler"""
    return jsonify({'error': 'Forbidden'}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
