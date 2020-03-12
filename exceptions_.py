class PyiPostError(Exception):
    pass


class PyiPostAuthenticationError(PyiPostError):
    pass


class PyiPostHTTPError(PyiPostError):
    pass
