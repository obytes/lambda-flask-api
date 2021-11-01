import os

from flask import Blueprint
from flask_restx import Api

from app.api.conf.settings import AWS_API_GW_MAPPING_KEY
from app.api.docs import get_swagger_ui
from app.api.errors.errors_handler import handle_errors

api_v1_blueprint = Blueprint('api', __name__, url_prefix=f'/v1')


class FlaskAPI(Api):

    @Api.base_path.getter
    def base_path(self):
        """
        The API path

        :rtype: str
        """
        return os.path.join(f"/{AWS_API_GW_MAPPING_KEY}", "v1")


authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'password',
        'tokenUrl': os.path.join(f"/{AWS_API_GW_MAPPING_KEY}", "v1/auth/token"),
        'refreshUrl': os.path.join(f"/{AWS_API_GW_MAPPING_KEY}", "v1/auth/refresh"),
    }
}

api_v1 = FlaskAPI(
    api_v1_blueprint,
    version='0.1.0',
    title="Lambda Flask API Starter",
    description="Fast API Starter, Deployed on AWS Lambda and served with AWS API Gateway",
    doc="/docs",
    authorizations=authorizations
)
api_v1.documentation(get_swagger_ui)
handle_errors(api_v1)
