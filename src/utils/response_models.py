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
from typing import Union, Optional, Dict
from datetime import date

from pydantic import BaseModel, EmailStr, constr


class SuccessOrNot(BaseModel):
    success: bool

### user ###
class UserBase(BaseModel):
    id: int
    username: str
    nickname: str
    birthday: date
    sex: int
    email: EmailStr
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

### administrative district ###

class AdministrativeDistrict(BaseModel):
    id: int
    area: str


### super charger
class SuperCharger(BaseModel):
    id: int
    name: str
    city: str
    tpc: Optional[int] = None
    ccs2: Optional[int] = None
    floor: Optional[str] = None
    business_hours: Optional[str] = None
    park_fee: Optional[str] = None
    charger_fee: Optional[str] = None
    version: Optional[str] = None