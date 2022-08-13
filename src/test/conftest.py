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

import os
from datetime import datetime
from random import choice

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database.db_handler import DBHandler
from database.models import Base
from utils.auth_tools import general_auth
from utils.const import Const

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test/test.db')
engine = create_engine(url=f'sqlite:///{db_path}?check_same_thread=False')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_general_auth():
    user = {
        'id': 1,
        'username': 'jimmy',
        'nickname': 'jimmy is not nick',
        'birthday': datetime(1996, 7, 19).date(),
        'sex': Const.Sex.MALE,
        'email': 'jimmy@gmail.com',
        'point': 0,
        'is_verified': True,
        'role': Const.Role.GENERAL,
        'charger_id': None,
        'exp': 1234567890
    }
    return user


@pytest.fixture(scope='module', autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[general_auth] = override_general_auth
    app.dependency_overrides[DBHandler.get_db] = override_get_db
    yield True

    os.remove(db_path)


@pytest.fixture(scope='class')
def user_info(request):
    user_info = {
        'username': 'jimmy',
        'password': '1234567890',
        'nickname': 'jimmy not nick',
        'email': 'chienfeng0719@hotmail.com',
        'birthday': datetime(1996, 7, 19).date(),
        'sex': choice(list(Const.Sex.get_elements())),
    }
    return user_info


@pytest.fixture(scope='class', params=[[
    {
        'model': 'Model S',
        'spec': 'Plaid',
    },
    {
        'model': 'Model X',
        'spec': 'Plaid＋',
    },
    {
        'model': 'Model 3',
        'spec': 'Performance'
    }
]])
def car_info(request):
    yield choice(request.param)
