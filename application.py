#!/usr/bin/env python
from app import app
# from flask import flask

# app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
