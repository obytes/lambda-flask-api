import logging

from flask import Blueprint
from flask_restx import Resource

from app.api.api_v1 import api_v1

manage_bp = Blueprint('manage', __name__, url_prefix='/v1/manage')
manage_ns = api_v1.namespace('manage', 'Operations related to management.')

logger = logging.getLogger(__name__)


@manage_ns.route('/hc')
class HealthCheck(Resource):

    def get(self):
        """
        Useful to prevent cold start, should be called periodically by another lambda
        """
        return {"status": "I'm sexy and I know It"}, 200
