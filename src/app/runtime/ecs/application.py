from __future__ import print_function

from flask import Flask
from flask_cors import CORS

from app.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app)
    register_blueprints(app)
    return app
