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
    users = User.search({'email': email})
    if users or len(users) > 0:
        # Validate the provided password
        is_pwd_valid = users[0].is_valid_password(password)
        if not is_pwd_valid:
            return ({"error": "wrong password"}), 401
    else:
        return ({"error": "no user found for this email"}), 400

    # If the user founds and valid password provide, create a session Id 
    from api.v1.app import auth
    user_id = users[0].id
    session_id = auth.create_session(user_id)
    
    # Jsonfiy to create a response object to set a cookie value
    cookie_name = os.getenv('SESSION_NAME')
    response_object = jsonify(users[0].to_json())
    response_object.set_cookie(cookie_name, session_id)

    return response_object


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
