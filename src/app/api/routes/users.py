import logging

from flask import Blueprint, g
from flask_restx import Resource

from app.api.api_v1 import api_v1
from app.api.decorators import auth

users_bp = Blueprint('users', __name__, url_prefix='/v1/users')
users_ns = api_v1.namespace('users', 'Operations related to users.')

logger = logging.getLogger(__name__)


@users_ns.route('/whoami')
class WhoAmI(Resource):

    @users_ns.doc(security=[{'oauth2': []}])
    @auth(allowed_groups=['USERS', 'ADMINS'])  # OR Simply @auth
    def get(self):
        """
        Return user specific JWT decoded claims
        """
        return {"claims": g.claims}, 200
