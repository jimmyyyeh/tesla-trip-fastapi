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
from typing import Optional, Union

from pydantic import BaseModel, validator, EmailStr


### user ###
from utils.const import Const


class SignIn(BaseModel):
    username: str
    password: str


class SignUp(BaseModel):
    username: str
    password: str
    nickname: Optional[str] = None
    email: EmailStr
    birthday: date
    sex: int

    @validator('sex')
    def valid_sex(cls, value):
        if value not in Const.Sex.get_elements():
            raise ValueError('sex must be 1 or 2')
        return value


class Verify(BaseModel):
    token: str


class ResendVerify(BaseModel):
    username: str


class RequestResetPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    username: str
    password: str


class UpdateProfile(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None

### car ###
class CreateCar(BaseModel):
    model: str
    spec: str
    manufacture_date: date
    file: Optional[str] = None


class UpdateCar(BaseModel):
    model: str
    spec: str
    manufacture_date: date


### trip ###
class CreateTrip(BaseModel):
    car_id: int
    mileage: int
    consumption: Union[int, float]
    total: Union[int, float]
    start: str
    end: str
    start_battery_level: int
    end_battery_level: int
    is_charge: bool
    charger_id: Optional[int] = None
    charge: Optional[int] = None
    fee: Optional[int] = None
    trip_date: date


class UpdateTripRate(BaseModel):
    trip_id: int


### qrcode ###
class EncodeProduct(BaseModel):
    product_id: int


### product ###
class CreateProduct(BaseModel):
    name: str
    stock: int
    point: int
    is_launched: bool


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    stock: Optional[str] = None
    point: Optional[int] = None
    is_launched: Optional[bool] = None
