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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database.db_handler import DBHandler
from database.models import Base
from utils.auth_tools import general_auth

engine = create_engine(url='sqlite:///test/test.db?check_same_thread=False')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestBase:
    """
    因為test folder下不能放__init__, 因此放在這裡
    """

    @staticmethod
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def override_general_auth():
        db = TestingSessionLocal()
        user = DBHandler.get_user_by_id(db=db, id_=1)
        user = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'birthday': user.birthday,
            'sex': user.sex,
            'email': user.email,
            'point': user.point,
            'is_verified': user.is_verified,
            'role': user.role,
            'charger_id': user.charger_id,
            'exp': 1234567890
        }
        db.close()
        return user

    def setup_class(self):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[general_auth] = self.override_general_auth
        app.dependency_overrides[DBHandler.get_db] = self.override_get_db

    @staticmethod
    def teardown_class():
        os.remove('./test/test.db')
