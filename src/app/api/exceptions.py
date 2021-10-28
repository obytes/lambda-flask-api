class LambdaValidationError(Exception):
    def __init__(self, message, fields=None):
        super(LambdaValidationError, self).__init__(message)
        self.fields = fields


class LambdaAuthorizationError(Exception):
    def __init__(self, errors=None):
        self.errors = errors
        if type(errors) is str:
            super(LambdaAuthorizationError, self).__init__(errors)


class LambdaHeaderNotSetError(Exception):
    def __init__(self, errors=None):
        self.errors = errors
        if type(errors) is str:
            super(LambdaHeaderNotSetError, self).__init__(errors)
