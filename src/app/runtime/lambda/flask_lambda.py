# -*- coding: utf-8 -*-

import base64
import sys

from app.api.conf.settings import AWS_API_GW_STAGE_NAME
from .warmer import warmer

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from flask import Flask
from io import BytesIO

from werkzeug._internal import _to_bytes


def strip_api_gw_stage_name(path: str) -> str:
    if path.startswith(f"/{AWS_API_GW_STAGE_NAME}"):
        return path[len(f"/{AWS_API_GW_STAGE_NAME}"):]
    return path


def adapt(event):
    environ = {'SCRIPT_NAME': ''}

    context = event['requestContext']
    http = context['http']

    # Construct HEADERS
    for hdr_name, hdr_value in event['headers'].items():
        hdr_name = hdr_name.replace('-', '_').upper()
        if hdr_name in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            environ[hdr_name] = hdr_value
            continue

        http_hdr_name = 'HTTP_%s' % hdr_name
        environ[http_hdr_name] = hdr_value

    # Construct QUERY Params
    qs = event.get('queryStringParameters')
    environ['QUERY_STRING'] = urlencode(qs) if qs else ''

    # Construct HTTP
    environ['REQUEST_METHOD'] = http['method']
    environ['PATH_INFO'] = strip_api_gw_stage_name(http['path'])
    environ['SERVER_PROTOCOL'] = http['protocol']
    environ['REMOTE_ADDR'] = http['sourceIp']
    environ['HOST'] = '%(HTTP_HOST)s:%(HTTP_X_FORWARDED_PORT)s' % environ
    environ['SERVER_PORT'] = environ['HTTP_X_FORWARDED_PORT']
    environ['wsgi.url_scheme'] = environ['HTTP_X_FORWARDED_PROTO']

    # Authorizer
    environ['AUTHORIZER'] = context.get('authorizer')
    environ['IDENTITY'] = context.get('identity')

    # Body
    body = event.get(u"body", "")
    if event.get("isBase64Encoded", False):
        body = base64.b64decode(body)
    if isinstance(body, (str,)):
        body = _to_bytes(body, charset="utf-8")
    environ['CONTENT_LENGTH'] = str(len(body))

    # WSGI
    environ['wsgi.input'] = BytesIO(body)
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = False
    environ['wsgi.run_once'] = True
    environ['wsgi.multiprocess'] = False

    return environ


class LambdaResponse(object):
    def __init__(self):
        self.status = None
        self.response_headers = None

    def start_response(self, status, response_headers, exc_info=None):
        self.status = int(status[:3])
        self.response_headers = dict(response_headers)


class FlaskLambda(Flask):

    @warmer(send_metric=False)
    def __call__(self, event, context):
        response = LambdaResponse()
        response_body = next(self.wsgi_app(
            adapt(event),
            response.start_response
        ))
        res = {
            'statusCode': response.status,
            'headers': response.response_headers,
            'body': response_body.decode("utf-8")
        }
        return res
