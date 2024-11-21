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
        auth.register_user(email, password)
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
    session_id = request.cookies.get('session_id', None)
    if session_id is None:
        abort(403)
    user = auth.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
