from flask import Blueprint
from flask_restx import Api

from app.api.errors.errors_handler import handle_errors
from app.api.conf import Conf

api_v1_blueprint = Blueprint('api', __name__, url_prefix=f'/{Conf.AWS_API_GW_STAGE_NAME}/v1')

api_v1 = Api(api_v1_blueprint,
             version='1.0',
             title='Demo Rest API',
             description='A demo is worth thousand words',
             doc='/docs')


handle_errors(api_v1)
