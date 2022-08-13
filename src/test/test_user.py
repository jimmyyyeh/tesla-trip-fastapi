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
from routes import user
from utils.response_models import Response, SignIn, SignUp, SuccessOrNot, UserBase

app = create_app()
app.include_router(user.router)

client = TestClient(app)


class TestUser:
    def test_sign_up(self, user_info: dict):
        response = client.post('/sign-up', json=user_info)
        assert response.status_code == 200
        assert Response[SignUp].validate(response.json())

    def test_verify(self, mocker: MockerFixture):
        mocker.patch('database.redis_handler.RedisHandler.get_verify_user', return_value=1)
        payload = {
            'token': str(uuid1())
        }
        response = client.post('/verify', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    def test_resend_verify(self, user_info: dict):
        payload = {
            'username': user_info['username']
        }
        response = client.post('/resend-verify', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    def test_sign_in(self, user_info: dict):
        payload = {
            'username': user_info['username'],
            'password': user_info['password']
        }
        response = client.post('/sign-in', json=payload)
        assert response.status_code == 200
        assert Response[SignIn].validate(response.json())

    def test_request_reset_password(self, user_info):
        payload = {
            'email': user_info['email']
        }
        response = client.post('/request-reset-password', json=payload)
        assert response.status_code == 200
        assert SuccessOrNot.validate(response.json())

    def test_request_password(self, mocker: MockerFixture, user_info: dict):
        mocker.patch('database.redis_handler.RedisHandler.get_reset_password', return_value=1)
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

    @staticmethod
    def test_update_profile():
        payload = {
            'email': 'jimmy@hotmial.com',
            'nickname': 'nick is not jimmy'
        }
        response = client.put('/profile', json=payload, headers={})
        assert response.status_code == 200
        assert Response[SignIn].validate(response.json())
