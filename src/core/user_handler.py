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

from secrets import token_hex

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from sqlalchemy.orm import Session

from config import Config
from database.crud import CRUD
from utils.auth_tools import AuthTools
from utils.payload_schemas import SignIn, SignUp
from utils.redis_handler import RedisHandler
from utils.tools import Tools


class UserHandler:

    @staticmethod
    async def _send_email(email, html):
        mail_config = ConnectionConfig(
            MAIL_USERNAME=Config.MAIL_USERNAME,
            MAIL_PASSWORD=Config.MAIL_PASSWORD,
            MAIL_FROM=f'{Config.MAIL_USERNAME}@gmail.com',
            MAIL_PORT=Config.MAIL_PORT,
            MAIL_SERVER=Config.MAIL_SERVER,
            MAIL_TLS=False,
            MAIL_SSL=Config.MAIL_USE_SSL,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        message = MessageSchema(
            subject='Tesla Trip 驗證信件',
            recipients=[email],
            html=html,
            subtype='html'
        )
        mail = FastMail(mail_config)
        await mail.send_message(message=message)

    @classmethod
    async def send_verify_mail(cls, email, id_):
        verify_token = token_hex(16)
        RedisHandler.set_verify_user(
            verify_token=verify_token,
            id_=id_
        )
        html = f"""
                <h1>歡迎註冊</h1>
                <body>
                    <p>歡迎您註冊Tesla Trip，請點選以下連結以進行驗證:</p>
                    <a href='{Config.WEB_DOMAIN}/#/verify/{verify_token}'>驗證連結</a>
                </body>
                """
        await cls._send_email(email=email, html=html)

    @staticmethod
    def sign_in(db: Session, payload: SignIn):
        user = CRUD.get_user(db=db, username=payload.username)
        verified = AuthTools.verify_password(password=payload.password, hashed_password=user.password)
        if not verified:
            # TODO raise
            ...
        if not user:
            # TODO raise
            ...
        result = {
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
        }
        Tools.serialize_result(dict_=result)
        access_token = AuthTools.create_access_token(data=result)
        result.update({'access_token': access_token, 'token_type': 'bearer'})
        return result

    @classmethod
    def sign_up(cls, db: Session, payload: SignUp):
        user = CRUD.get_user(db=db, username=payload.username, email=payload.email)
        if user:
            # TODO raise
            ...
        user = CRUD.create_user(
            db=db,
            username=payload.username,
            password=payload.password,
            nickname=payload.nickname,
            email=payload.email,
            birthday=payload.birthday,
            sex=payload.sex
        )
        result = {
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
        }
        return result
