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
from typing import Union
from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    nickname: str
    birthday: date
    sex: int
    email: str
    point: int
    is_verified: bool
    role: int
    charger_id: Union[int, None]

    class Config:
        orm_mode = True


class SignUp(UserBase):
    ...


class SignIn(UserBase):
    access_token: str
    token_type: str
