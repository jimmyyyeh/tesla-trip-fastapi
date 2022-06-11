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

from datetime import date
from typing import Union, Optional

from pydantic import BaseModel, EmailStr


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


### car
class Car(BaseModel):
    id: int
    car: Optional[str]= None
    model: str
    spec: str
    manufacture_date: date
    has_image: bool

class CarModel(BaseModel):
    id: int
    model: str
    spec: str

class CarDeductPoint(BaseModel):
    total: int
