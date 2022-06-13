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

from datetime import timedelta, datetime
from typing import Optional

from fastapi import Header, Request, status, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from config import Config
from utils.error_codes import ErrorCodes
from utils.errors import AuthException
from utils.pattern import Pattern


class AuthTools:
    _PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @staticmethod
    def create_access_token(data, expires_delta=None):
        encode_data = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode_data.update({'exp': expire})
        encoded_jwt = jwt.encode(encode_data, key=Config.SALT, algorithm='HS256')

        return encoded_jwt

    @classmethod
    def verify_password(cls, password, hashed_password):
        return cls._PWD_CONTEXT.verify(password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls._PWD_CONTEXT.hash(password)


class AuthValidator(HTTPBearer):
    def __init__(self, roles=None):
        super().__init__()
        self.roles = roles or list()

    async def __call__(self, request: Request) -> dict:
        try:
            r = await super().__call__(request)
            token = r.credentials
            user = jwt.decode(token=token, key=Config.SALT)
            if self.roles and user['role'] not in self.roles:
                raise AuthException(
                    error_msg='role invalidate',
                    error_code=ErrorCodes.ROLE_INVALIDATE
                )
            return user
        except (JWTError, HTTPException) as e:
            raise AuthException(
                error_msg='token invalidate',
                error_code=ErrorCodes.TOKEN_INVALIDATE
            )
