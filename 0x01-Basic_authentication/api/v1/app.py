#!/usr/bin/env python3
"""
Route module for the API.

This script initializes a Flask application, configures it with CORS, and sets up authentication
based on the environment variable AUTH_TYPE. It registers the blueprint for API routes and handles
requests with appropriate error responses.

Dependencies:
- Flask: Web framework for building the application.
- Flask-CORS: Middleware for handling Cross-Origin Resource Sharing (CORS).

Environment Variables:
- AUTH_TYPE: Specifies the type of authentication to use (e.g., 'auth'). If not set, no authentication is applied.
- API_HOST: Host IP address to run the Flask application. Defaults to '0.0.0.0'.
- API_PORT: Port number to run the Flask application. Defaults to '5000'.

Routes:
- /api/v1/status/ - Returns the status of the API.
- /api/v1/unauthorized/ - Triggers a 401 Unauthorized error.
- /api/v1/forbidden/ - Triggers a 403 Forbidden error.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)

# Register the blueprint for API routes
app.register_blueprint(app_views)
print("Blueprint registered")

# Configure CORS to allow all origins for API routes
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication
auth = None
auth_type = getenv("AUTH_TYPE")

# List of routes that require authentication
access_routes = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

# Conditionally import and set up authentication based on AUTH_TYPE environment variable
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()

@app.before_request
def b4_request() -> None:
    """
    Called before each request to handle authentication and authorization.

    - If `auth` is None, skips authentication checks.
    - If the request path does not require authentication, skips further checks.
    - Checks if the request has an Authorization header. If not, aborts with 401 Unauthorized.
    - Checks if a valid user is associated with the request. If not, aborts with 403 Forbidden.
    """
    if auth is None:
        return  # Skip authorization checks if auth is not initialized

    # Check if authentication is required for the request path
    if not auth.require_auth(request.path, access_routes):
        return  # Skip further checks if authentication is not required

    # Check for Authorization header
    if auth.authorization_header(request) is None:
        abort(401)  # Abort with 401 Unauthorized if the header is missing

    # Check for current user
    if auth.current_user(request) is None:
        abort(403)  # Abort with 403 Forbidden if the user is not valid

@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles 401 Unauthorized errors.

    Returns a JSON response with an error message and a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles 403 Forbidden errors.

    Returns a JSON response with an error message and a 403 status code.
    """
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles 404 Not Found errors.

    Returns a JSON response with an error message and a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Run the Flask application with specified host and port
    host = getenv("API_HOST", "0.0.0.0")  # Default to '0.0.0.0' if not set
    port = getenv("API_PORT", "5000")     # Default to '5000' if not set
    app.run(host=host, port=port)
