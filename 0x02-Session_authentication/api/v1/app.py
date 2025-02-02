#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


# This paths are excluded from authentication
excluded_paths = [
        '/api/v1/status/', '/api/v1/unauthorized/',
        '/api/v1/forbidden/', '/api/v1/auth_session/login/']

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH_TYPE = getenv('AUTH_TYPE')

if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()

if AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

if AUTH_TYPE == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()


@app.before_request
def before_request():
    """Handle everythin before any route handler is called"""
    if auth is None:
        return
    # Get path from request
    request_path = request.path

    # check if the path requires authentication
    is_valid_path = auth.require_auth(request_path, excluded_paths)
    if is_valid_path:
        # If no authorization header provided
        if not auth.authorization_header(request):
            if not auth.session_cookie(request):
                abort(401)
        # If the user is not valid
        if not auth.current_user(request):
            abort(403)
    # Assign current user
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_access(error) -> str:
    """ Unauthorized access error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Forbidden access error """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
