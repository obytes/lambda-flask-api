import logging

import requests
from flask import Blueprint, request
from flask_restx import Resource

from app.api.api_v1 import api_v1
from app.api.conf.settings import FIREBASE_APP_API_KEY
from app.api.exceptions import LambdaAuthorizationError

auth_bp = Blueprint('auth', __name__, url_prefix='/v1/auth')
auth_ns = api_v1.namespace('auth', 'Operations related to auth.')

logger = logging.getLogger(__name__)


@auth_ns.route("/token")
class Token(Resource):

    def post(self):
        base_path = "https://identitytoolkit.googleapis.com"
        payload = {
            "email": request.form["username"],
            "password": request.form["password"],
            'returnSecureToken': True
        }
        # Post request
        r = requests.post(
            f"{base_path}/v1/accounts:signInWithPassword?key={FIREBASE_APP_API_KEY}",
            data=payload
        )
        keys = r.json().keys()
        # Check for errors
        if "error" in keys:
            error = r.json()["error"]
            raise LambdaAuthorizationError(
                errors=error["message"]
            )
        # success
        auth = r.json()
        auth["token_type"] = "bearer"
        auth["access_token"] = auth.pop("idToken")
        return auth
