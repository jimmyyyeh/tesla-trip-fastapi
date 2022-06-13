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
from fastapi import FastAPI
from sqlalchemy import create_engine

from config import Config

app = FastAPI()

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
