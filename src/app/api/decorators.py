from functools import wraps
from typing import List

from flask import g, request

from app.api.conf import Conf
from app.api.exceptions import LambdaAuthorizationError
from app.api.auth import decode_jwt_token


def get_claims():
    g.access_token = request.headers.get('Authorization').split()[1]
    if Conf.RUNTIME == 'LAMBDA':
        g.claims = request.environ['AUTHORIZER']['jwt']['claims']
        g.username = g.claims['sub']
        g.groups = g.claims.get(Conf.JWT_AUTHORIZATION_GROUPS_ATTR_NAME, "[]").strip("[]").split()
    elif Conf.RUNTIME == 'CONTAINERIZED':
        g.claims = decode_jwt_token(g.access_token)
        g.username = g.claims['sub']
        g.groups = g.claims.get(Conf.JWT_AUTHORIZATION_GROUPS_ATTR_NAME, [])
    else:
        raise Exception("No runtime specified, Please set RUNTIME environment variable!")


def auth(_route=None, allowed_groups: List = None):
    def decorator(route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            get_claims()
            if allowed_groups:
                if not g.groups:
                    raise LambdaAuthorizationError(
                        'The endpoint has authorization check and the caller does not belong to any groups'
                    )
                else:
                    if not any(group in allowed_groups for group in g.groups):
                        raise LambdaAuthorizationError(f'Only {allowed_groups} can access this endpoint')
            return route(*args, **kwargs)

        return wrapper

    if _route:
        return decorator(_route)
    return decorator
