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

from typing import Optional, Union
from pydantic import BaseModel, constr, validator


class SignIn(BaseModel):
    username: str
    password: str


class SignUp(BaseModel):
    username: str
    password: str
    nickname: Optional[str] = None
    email: constr(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
    birthday: str
    sex: int

    @validator('sex')
    def valid_sex(cls, value):
        if value not in {0, 1}:
            raise ValueError('sex must be 1 or 0')
        return value


class Verify(BaseModel):
    token: str


class ResendVerify(BaseModel):
    username: str


class RequestResetPassword(BaseModel):
    email: constr(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')


class ResetPassword(BaseModel):
    token: str
    username: str
    password: str


class UpdateProfile(BaseModel):
    email: Optional[constr(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')] = None
    nickname: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str


class CreateCar(BaseModel):
    model: str
    spec: str
    manufacture_date: str
    file: Optional[str] = None


class UpdateCar(BaseModel):
    model: str
    spec: str
    manufacture_date: str


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
    trip_date: str


class UpdateTripRate(BaseModel):
    trip_id: int


class EncodeProduct(BaseModel):
    product_id: int


class CreateProduct(BaseModel):
    name: str
    stock: str
    point: int
    is_launched: bool


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    stock: Optional[str] = None
    point: Optional[int] = None
    is_launched: Optional[bool] = None
