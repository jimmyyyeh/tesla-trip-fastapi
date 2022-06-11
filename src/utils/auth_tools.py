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

    @classmethod
    def verify_auth(cls, authorization: str = Header()):
        token = authorization.split(' ')[1]
        try:
            user = jwt.decode(token=token, key=Config.SALT)
            return user
        except JWTError as e:
            # TODO raise
            ...
