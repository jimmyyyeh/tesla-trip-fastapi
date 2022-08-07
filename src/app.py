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

from urllib.parse import quote

import redis
from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi
from sqlalchemy import create_engine
from starlette.middleware.cors import CORSMiddleware

from settings import Settings
from utils.error_codes import ErrorCodes
from utils.response_models import Error

responses = {
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
                'example': {'error_msg': 'user does not exist', 'error_code': ErrorCodes.USER_NOT_EXISTS}
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
}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='tesla trip api',
        version='0.0.1',
        description='The api doc of tesla trip api',
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app():
    return app


app = FastAPI(responses=responses)
app.openapi = custom_openapi

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

settings = Settings()

redis_instance = redis.StrictRedis(
    host=settings.redis_host,
    password=settings.redis_password,
    port=settings.redis_port,
    encoding='utf-8',
    decode_responses=True,
)

url = f'mysql+pymysql://' \
      f'{settings.mysql_user}:%s@{settings.mysql_host}:{settings.mysql_port}/{settings.db_name}' \
      % quote(settings.mysql_password)

engine = create_engine(url=url)
