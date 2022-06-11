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
from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import User
from utils.auth_tools import AuthTools


class CRUD:
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def get_user_by_id(db: Session, id_: str):
        user = db.query(User).filter(User.id == id_).first()
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str, email: EmailStr = None):
        if email:
            conditions = [or_(User.username == username,
                              User.email == email)]
        else:
            conditions = [User.username == username]
        user = db.query(User).filter(*conditions).first()
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr):
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def create_user(db: Session, username: str, password: str, nickname: str, email: EmailStr, birthday: str, sex: int):
        user = User(
            username=username,
            password=AuthTools.get_password_hash(password=password),
            nickname=nickname,
            email=email,
            birthday=birthday,
            sex=sex
        )
        db.add(user)
        db.commit()
        # TODO send email
        return user
