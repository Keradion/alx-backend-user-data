#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Retrun JSON Payload"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
