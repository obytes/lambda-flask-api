from __future__ import print_function

from app.blueprints import register_blueprints
from .flask_lambda import FlaskLambda


def create_app():
    # Init app
    app = FlaskLambda(__name__)
    app.url_map.strict_slashes = False
    app.config["RESTX_JSON"] = {"indent": 4}
    register_blueprints(app)
    return app


handler = create_app()
