#!/usr/bin/env python3
"""Session Authentication"""
import os
from api.v1.views import app_views
from flask import Flask, request, jsonify
from models.user import User


# Create a Flask app
app = Flask(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """A route to handle login process"""
    # Retrieve user Email from form
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    # Retrieve user Password from form
    password = request.form.get('password')
    if not password:
        return ({"error": "password missing"}), 400

    # Retrieve User instance based on the email provided
    try:
        find_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    
    if not find_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in find_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    # If the user founds and valid password provide, create a session Id
    from api.v1.app import auth
    user = find_users[0]
    user_id = user.id
    session_id = auth.create_session(user_id)
    # Jsonfiy to create a response object to set a cookie value
    cookie_name = os.getenv('SESSION_NAME')
    response_object = jsonify(user.to_json())
    response_object.set_cookie(cookie_name, session_id)

    return response_object


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """A route to handle logout process"""
    from api.v1.app import auth
    is_deleted = auth.destroy_session(request)
    if is_deleted:
        return jsonify({}), 200
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
