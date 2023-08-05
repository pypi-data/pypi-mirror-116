from aduck import error_codes

class Error(Exception):

    def __init__(self, code: int, message: str, module: str = None, detail=None, e: Exception = None, **kwargs):
        super(Error, self).__init__()
        self.code = code
        self.message = message
        self.module = module
        self.detail = detail
        self.kwargs = kwargs
        self._exception = e

    def __str__(self):
        return f"module:{self.module},error code:{self.code},message:{self.message}"

    def __repr__(self):
        return self.__str__()


class UserError(Error):
    """
    UserError should be handed over to user(client)
    """

    def __init__(self, code, message, module: str = None, detail=None, e: Exception = None, **kwargs):
        super(UserError, self).__init__(code, message, module, detail, e=e, **kwargs)


class FieldError(UserError):

    def __init__(self, code, message, field_errors: dict = None, module: str = None, detail=None, e: Exception = None,
                 **kwargs):
        super(FieldError, self).__init__(code, message, module, detail, e=e, **kwargs)
        self.field_errors = field_errors or {}

    def add_field_error(self, field: str, message: str):
        self.field_errors[field] = message
