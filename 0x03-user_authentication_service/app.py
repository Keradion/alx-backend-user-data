#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Retrun JSON Payload"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
