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

import redis
from fastapi import FastAPI, status
from sqlalchemy import create_engine

from config import Config
from utils.error_codes import ErrorCodes
from utils.response_models import Error

app = FastAPI(responses={
    400: {
        'model': Error, 'description': 'Bad request',
        'content': {
            'application/json': {
                'example': {'error_msg': 'bad request', 'error_code': status.HTTP_400_BAD_REQUEST}
            }
        },
    },
    401: {
        'model': Error, 'description': 'Auth failed',
        'content': {
            'application/json': {
                'example': {'error_msg': 'user not exists', 'error_code': ErrorCodes.USER_NOT_EXISTS}
            }
        },
    },
    404: {
        'model': Error, 'description': 'Data not found',
        'content': {
            'application/json': {
                'example': {'error_msg': 'data not found', 'error_code': status.HTTP_404_NOT_FOUND}
            }
        },
    },
    422: {
        'model': Error, 'description': 'Unprocessable entity',
        'content': {
            'application/json': {
                'example': {'error_msg': 'unprocessable entity', 'error_code': status.HTTP_422_UNPROCESSABLE_ENTITY}
            }
        },
    },
    500: {
        'model': Error, 'description': 'Internal server error',
        'content': {
            'application/json': {
                'example': {'error_msg': 'internal server error', 'error_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
            }
        },
    },
})

redis_instance = redis.StrictRedis(
    host=Config.REDIS_HOST,
    password=Config.REDIS_PASSWORD,
    port=Config.REDIS_PORT,
    charset='utf-8',
    decode_responses=True,
)

engine = create_engine(url=Config.SQLALCHEMY_DATABASE_URL)


def create_app():
    return app
