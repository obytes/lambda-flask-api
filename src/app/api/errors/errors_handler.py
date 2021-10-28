import logging

from jose import JWTError

from app.api.exceptions import LambdaValidationError, LambdaAuthorizationError, LambdaHeaderNotSetError

logger = logging.getLogger(__name__)


def handle_errors(api):
    # Custom exceptions
    # ----------------
    @api.errorhandler(JWTError)
    def handle_jwt_exception(error):
        exception = {
                        'error': {
                            'code': '001401',
                            'title': 'Invalid JWT Token',
                            'message': 'Access Unauthorized!',
                            'reason': str(error),
                        }
                    }, 401
        logger.exception(exception, extra={'stack': True})
        return exception

    @api.errorhandler(LambdaAuthorizationError)
    def handle_authorization_exception(error):
        return {
                   'error': {
                       'code': '002401',
                       'title': 'Unauthorized',
                       'message': 'Access unauthorized',
                       'reason': str(error),
                   }
               }, 401

    @api.errorhandler(LambdaValidationError)
    def handle_validation_exception(error):
        return {
                   'error': {
                       'code': '001400',
                       'title': 'Validation Error',
                       'message': 'One or more incorrect fields',
                       'reason': str(error),
                       'fields': error.fields
                   }
               }, 400

    @api.errorhandler(LambdaHeaderNotSetError)
    def handle_header_not_set_exception(error):
        return {
                   'error': {
                       'code': '002400',
                       'title': 'HTTP Header not set',
                       'message': 'Frontend team, read the docs!',
                       'reason': str(error),
                   },
               }, 400

    ########
    # Keep `Exception handler` at the end of the file as it's too broad
    ########
    @api.errorhandler(Exception)
    def handle_exception(error):
        logging.error(error)
        return {
                   'error': {
                       'code': '001500',
                       'title': 'Internal error',
                       'message': 'Oops, something went wrong!',
                       'reason': str(error),
                   }
               }, 400
