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

from fastapi import Header
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


class AuthValidator:
    def __init__(self, roles=None):
        self.roles = roles or list()

    def __call__(self, authorization: str = Header()):
        token = Pattern.BEARER_TOKEN.search(authorization).group(2)
        try:
            user = jwt.decode(token=token, key=Config.SALT)
            if self.roles and user['role'] not in self.roles:
                raise AuthException(
                    error_msg='role invalidate',
                    error_code=ErrorCodes.ROLE_INVALIDATE
                )
            return user
        except JWTError as e:
            raise AuthException(
                error_msg='token invalidate',
                error_code=ErrorCodes.TOKEN_INVALIDATE
            )
