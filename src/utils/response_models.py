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
from typing import Optional, List, Dict, Union, Generic, TypeVar

from fastapi import status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, EmailStr
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class SuccessOrNot(BaseModel):
    success: bool


class Pager(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int


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
    car: Optional[str] = None
    model: str
    spec: str
    manufacture_date: Union[date, str]
    has_image: bool


class CarModel(BaseModel):
    id: int
    model: str
    spec: str


class CarDeductPoint(BaseModel):
    total: int


### product ###
class Product(BaseModel):
    id: int
    name: str
    stock: int
    point: int
    is_launched: bool


### qrcode ###
class DecodeProduct(BaseModel):
    id: int
    name: str
    user_id: int
    point: int

class EncodeProduct(BaseModel):
    image: str


### trip ###
class Trip(BaseModel):
    id: int
    mileage: int
    consumption: Union[int, float]
    total: Union[int, float]
    start: str
    end: str
    start_battery_level: int
    end_battery_level: int
    car: str
    trip_date: date
    is_rate: bool
    is_charge: bool
    trip_rate_count: Optional[int] = None
    charge: Optional[int] = None
    charger: Optional[str] = None
    fee: Optional[int] = None


class Error(BaseModel):
    error_msg: str
    error_code: int


class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    pager: Optional[Pager] = None


class ResponseHandler:
    @staticmethod
    def response(result, pager=None, status_code=status.HTTP_200_OK):
        if isinstance(result, bool):
            return ORJSONResponse(content={'success': result}, status_code=status_code)
        else:
            return ORJSONResponse(content={'data': result, 'pager': pager}, status_code=status_code)
