#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth

app = Flask(__name__)

auth = Auth()


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
def login() -> str:
    """ endpoint to handle user login. """
    email = request.form.get('email')
    password = request.form.get('password')

    is_valid_user = auth.valid_login(email, password)
    if is_valid_user:
        user_session_id = auth.create_session(email)
        msg = {"email": email, "message": "logged in"}
        response = jsonify(msg)
        response.set_cookie('session_id', user_session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ endpoint to handle user logout process """
    session_id = request.cookies.get('session_id', None)
    if session_id is None:
        abort(403)
    user = auth.get_user_from_session_id(session_id)
    if user:
        auth.destroy_session(user.id)
        return redirect ('/')

    abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
