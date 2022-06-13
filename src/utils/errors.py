# -*- coding: utf-8 -*
"""
      ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
      ┗┳        ┗━┓
       ┃          ┣┓
       ┃          ┏┛
       ┗┓┓┏━━━━┳┓┏┛
        ┃┫┫    ┃┫┫
        ┗┻┛    ┗┻┛
    God Bless,Never Bug
"""

from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from loguru import logger

from app import app
from utils.error_codes import ErrorCodes


def make_error_schema(error_code, error_msg):
    _dict = {
        'error_code': error_code,
        'error_msg': error_msg
    }
    return _dict


class _BaseError(Exception):
    """
        base error class
    """

    def __init__(self, code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_msg=None, error_code=None):
        super(_BaseError, self).__init__()
        self.code = code
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return self.__class__.__name__

    def to_dict(self):
        return make_error_schema(
            error_msg=self.error_msg, error_code=self.error_code)


class AuthException(_BaseError):
    def __init__(self, error_msg=None, error_code=None):
        super(AuthException, self).__init__(
            code=status.HTTP_401_UNAUTHORIZED, error_msg=error_msg, error_code=error_code
        )


class ValidationException(_BaseError):
    def __init__(self, error_msg=None, error_code=None):
        super(ValidationException, self).__init__(
            code=status.HTTP_400_BAD_REQUEST, error_msg=error_msg, error_code=error_code
        )


class NotFoundException(_BaseError):
    def __init__(self, error_msg=None, error_code=None):
        super(NotFoundException, self).__init__(
            code=status.HTTP_404_NOT_FOUND, error_msg=error_msg, error_code=error_code
        )


@app.exception_handler(AuthException)
def auth_exception_handler(request, exc):
    return JSONResponse(content=exc.to_dict(),
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        headers={'WWW-Authenticate': 'basic'})


@app.exception_handler(ValidationException)
def validation_exception_handler(request, exc):
    return JSONResponse(content=exc.to_dict(), status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NotFoundException)
def not_found_exception_handler(request, exc):
    return JSONResponse(content=exc.to_dict(), status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request, exc):
    logger.exception(exc.json())
    return JSONResponse(content=make_error_schema(
        error_msg='parameter error',
        error_code=ErrorCodes.PARAMETER_ERROR,
    ), status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(PydanticValidationError)
def pydantic_validation_exception_handler(request, exc):
    logger.exception(exc.json())
    return JSONResponse(content=make_error_schema(
        error_msg='server error',
        error_code=ErrorCodes.INTERNAL_SERVER_ERROR,
    ), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
