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

from uuid import uuid1

from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture

from app import create_app
from database.models import User
from routes import user
from utils.const import Const
from utils.response_models import Response, SignIn, SignUp, SuccessOrNot, UserBase

app = create_app()
app.include_router(user.router)

client = TestClient(app)


class TestUser:
    @staticmethod
    def _get_user(user_info: dict, is_verified=True):
        user_ = User(
            id=1,
            username=user_info['username'],
            password=user_info['password'],
            nickname=user_info['nickname'],
            email=user_info['email'],
            birthday=user_info['birthday'],
            sex=user_info['sex'],
            point=0,
            is_verified=is_verified,
            role=Const.Role.GENERAL,
        )
        return user_

    def test_sign_up(self, user_info: dict):
        payload = user_info.copy()
        payload['birthday'] = payload['birthday'].strftime('%Y-%m-%d')
        response = client.post('/sign-up', json=payload)
        assert response.status_code == 200
        assert Response[SignUp].validate(response.json())

    def test_verify(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.redis_handler.RedisHandler.get_verify_user', return_value=1)
        mocker.patch('database.db_handler.DBHandler.get_user_by_id',
                     return_value=self._get_user(user_info=user_info))
        payload = {
            'token': str(uuid1())
        }
        response = client.post('/verify', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    def test_resend_verify(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.db_handler.DBHandler.get_user_by_username',
                     return_value=self._get_user(user_info=user_info))
        payload = {
            'username': user_info['username']
        }
        response = client.post('/resend-verify', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    def test_sign_in(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.db_handler.DBHandler.get_user_by_username',
                     return_value=self._get_user(user_info=user_info))
        mocker.patch('utils.auth_tools.AuthTools.verify_password',
                     return_value=True)
        payload = {
            'username': user_info['username'],
            'password': user_info['password']
        }
        response = client.post('/sign-in', json=payload)
        assert response.status_code == 200
        assert Response[SignIn].validate(response.json())

    def test_unverified_sign_in(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.db_handler.DBHandler.get_user_by_username',
                     return_value=self._get_user(user_info=user_info, is_verified=False))
        mocker.patch('utils.auth_tools.AuthTools.verify_password',
                     return_value=True)
        payload = {
            'username': user_info['username'],
            'password': user_info['password']
        }
        response = client.post('/sign-in', json=payload)
        assert response.status_code == 401

    def test_request_reset_password(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.db_handler.DBHandler.get_user_by_email',
                     return_value=self._get_user(user_info=user_info))
        payload = {
            'email': user_info['email']
        }
        response = client.post('/request-reset-password', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    def test_request_password(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.redis_handler.RedisHandler.get_reset_password', return_value=1)
        mocker.patch('database.db_handler.DBHandler.get_user_by_id',
                     return_value=self._get_user(user_info=user_info))
        payload = {
            'token': str(uuid1()),
            'username': user_info['username'],
            'password': str(uuid1()),
        }
        response = client.post('/reset-password', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    @staticmethod
    def test_get_profile():
        response = client.get('/profile', headers={})
        assert response.status_code == 200
        assert Response[UserBase].validate(response.json())

    def test_update_profile(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.db_handler.DBHandler.get_user_by_id',
                     return_value=self._get_user(user_info=user_info))
        payload = {
            'email': 'jimmy@hotmail.com',
            'nickname': 'nick is not jimmy'
        }
        response = client.put('/profile', json=payload, headers={})
        assert response.status_code == 200
        assert Response[SignIn].validate(response.json())
