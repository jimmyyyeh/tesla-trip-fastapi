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
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import settings
from database.db_handler import DBHandler
from database.redis_handler import RedisHandler
from utils.auth_tools import AuthTools
from utils.error_codes import ErrorCodes
from utils.errors import AuthException, ValidationException
from utils.payload_schemas import SignIn, SignUp
from utils.tools import Tools


class UserHandler:

    @staticmethod
    async def _send_email(subject, email, html):
        mail_config = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=EmailStr(f'{settings.mail_username}@gmail.com'),
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_TLS=False,
            MAIL_SSL=settings.mail_use_ssl,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            html=html,
            subtype='html'
        )
        mail = FastMail(mail_config)
        await mail.send_message(message=message)

    @classmethod
    async def send_verify_mail(cls, id_: int, email: str):
        verify_token = token_hex(16)
        RedisHandler.set_verify_user(
            verify_token=verify_token,
            id_=id_
        )
        html = f"""
                <h1>歡迎註冊</h1>
                <body>
                    <p>歡迎您註冊Tesla Trip，請點選以下連結以進行驗證:</p>
                    <a href='{settings.web_domain}/#/verify/{verify_token}'>驗證連結</a>
                </body>
                """
        await cls._send_email(subject='Tesla Trip 驗證信件', email=email, html=html)

    @classmethod
    async def send_reset_password_mail(cls, id_: int, email: str):
        reset_token = token_hex(16)
        RedisHandler.set_reset_password(
            reset_token=reset_token,
            id_=id_,
        )
        html = f"""
                <h1>重設密碼</h1>
                <body>
                    <p>親愛的Tesla Trip用戶您好，請點選以下連結以進行重置密碼:</p>
                    <a href='{settings.web_domain}/#/resetPassword/{reset_token}'>重設密碼連結</a>
                </body>
                """
        await cls._send_email(subject='Tesla Trip 重設密碼信件', email=email, html=html)

    @classmethod
    async def sign_in(cls, db: Session, payload: SignIn):
        user = DBHandler.get_user_by_username(db=db, username=payload.username)
        if not user:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        validated = AuthTools.verify_password(password=payload.password, hashed_password=user.password)
        if not validated:
            raise AuthException(
                error_msg='user invalidate',
                error_code=ErrorCodes.USER_INVALIDATE
            )
        if not user.is_verified:
            raise AuthException(
                error_msg='user unverified',
                error_code=ErrorCodes.USER_UNVERIFIED
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
        Tools.serialize_result(dict_=result)
        access_token = AuthTools.create_access_token(data=result)
        result.update({'access_token': access_token, 'token_type': 'bearer'})
        return result

    @classmethod
    async def sign_up(cls, db: Session, payload: SignUp):
        user = DBHandler.get_user_by_username(db=db, username=payload.username, email=payload.email)
        if user:
            raise AuthException(
                error_msg='user already exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        user = DBHandler.create_user(
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
        Tools.serialize_result(dict_=result)
        return result

    @staticmethod
    async def verify(db: Session, verify_token: str):
        id_ = RedisHandler.get_verify_user(
            verify_token=verify_token
        )
        if not id_:
            raise ValidationException(
                error_msg='token does not exist',
                error_code=ErrorCodes.VERIFY_TOKEN_NOT_EXISTS
            )
        user = DBHandler.get_user_by_id(
            db=db,
            id_=id_
        )
        if not user:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        user.is_verified = True
        db.commit()
        RedisHandler.delete_verify_user(verify_token=verify_token)
        return True

    @staticmethod
    async def resend_verify(db: Session, username: str):
        user = DBHandler.get_user_by_username(db=db, username=username)
        if not user:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        result = {
            'id': user.id,
            'email': user.email
        }
        return result

    @staticmethod
    async def request_reset_password(db: Session, email: EmailStr):
        user = DBHandler.get_user_by_email(
            db=db, email=email
        )
        if not user:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        result = {
            'id': user.id,
            'email': user.email
        }
        return result

    @staticmethod
    async def reset_password(db: Session, reset_token: str, username: str, password: str):
        id_ = RedisHandler.get_reset_password(
            reset_token=reset_token
        )
        if not id_:
            raise AuthException(
                error_msg='token does not exist',
                error_code=ErrorCodes.RESET_PASSWORD_TOKEN_NOT_EXISTS
            )
        user = DBHandler.get_user_by_id(db=db, id_=id_)
        if not user:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        if user.username != username:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        user.password = AuthTools.get_password_hash(password=password)
        db.commit()
        RedisHandler.delete_reset_password(reset_token=reset_token)
        return True

    @staticmethod
    async def update_profile(db: Session, user: dict, email: EmailStr, nickname: str):
        user = DBHandler.get_user_by_id(db=db, id_=user['id'])
        if not user:
            raise AuthException(
                error_msg='user does not exist',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        if nickname:
            user.nickname = nickname
        if email:
            user.email = email
        db.commit()
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
