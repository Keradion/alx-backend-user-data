#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Retrun JSON Payload"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ endpoint to register a user. """
    # Fetch email and pwd from post request
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        msg = {"email": email, "message": "user created"}
        return jsonify(msg)
    except ValueError:
        msg = {"message": "email already registered"}
        return jsonify(msg), 400


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    """ endpoint to handle user login. """
    email = request.form.get('email')
    password = request.form.get('password')

    is_valid_user = AUTH.valid_login(email, password)
    if not is_valid_user:
        abort(401)

    user_session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    response.set_cookie('session_id', user_session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """ endpoint to handle user logout process """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ Response for profile access from a user."""
    session_id = request.cookies.get('session_id', None)
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    msg = {"email": user.email}
    return jsonify(msg), 200


@app.route('/reset_password', methods=['POST'])
def reset_reset_password_token() -> str:
    """ endpoint to handle reset_token request. """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)

    msg = {"email": email, "reset_token": reset_token}
    response = jsonify(msg)
    return response, 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ endpoint to handle password update. """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    msg = {'email': email, 'message': 'password updated'}
    response = jsonify(msg)
    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
