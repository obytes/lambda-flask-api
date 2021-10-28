import logging

from flask import Blueprint, current_app, url_for
from flask_restx import Resource

from app.api.api_v1 import api_v1
from app.api.decorators import auth

admins_bp = Blueprint('admins', __name__, url_prefix='/v1/admins')
admins_ns = api_v1.namespace('admins', 'Operations related to admins.')

logger = logging.getLogger(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@admins_ns.route('/site-map')
class ListSiteMap(Resource):

    @auth(allowed_groups=['ADMINS'])
    def get(self):
        """
        Get flask app available urls
        """
        links = []
        for rule in current_app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return {"links": links}, 200
