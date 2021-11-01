import logging

from flask import Blueprint, current_app, url_for
from flask_restx import Resource

from app.api.api_v1 import api_v1
from app.api.decorators import auth

admin_bp = Blueprint('admin', __name__, url_prefix='/v1/admin')
admin_ns = api_v1.namespace('admin', 'Operations related to administration')

logger = logging.getLogger(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@admin_ns.route('/endpoints')
class ListEndpoints(Resource):

    @admin_ns.doc(security=[{'oauth2': []}])
    @auth(allowed_groups=['ADMINS'])
    def get(self):
        """
        Get flask app available urls
        """
        endpoints = []
        for rule in current_app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                endpoints.append({"path": url, "name": rule.endpoint})
        return {"endpoints": endpoints}, 200
