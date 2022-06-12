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
from typing import Optional, List, Dict
from typing import Union

from pydantic import BaseModel, EmailStr


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


class SignUpBase(UserBase):
    ...


class SignUp(BaseModel):
    data: SignUpBase
    pager: Optional[Pager] = None


class SignInBase(UserBase):
    access_token: str
    token_type: str


class SignIn(BaseModel):
    data: SignInBase
    pager: Optional[Pager] = None


### administrative district ###

class AdministrativeDistrictBase(BaseModel):
    id: int
    area: str


class AdministrativeDistrict(BaseModel):
    data: Dict[str, List[AdministrativeDistrictBase]]
    pager: Optional[Pager] = None


### super charger
class SuperChargerBase(BaseModel):
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


class SuperCharger(BaseModel):
    data: List[SuperChargerBase]
    pager: Optional[Pager] = None


### car
class CarBase(BaseModel):
    id: int
    car: Optional[str] = None
    model: str
    spec: str
    manufacture_date: date
    has_image: bool


class Car(BaseModel):
    data: Union[List[CarBase], CarBase]
    pager: Optional[Pager] = None


class CarModelBase(BaseModel):
    id: int
    model: str
    spec: str


class CarModel(BaseModel):
    data: CarModelBase
    pager: Optional[Pager] = None


class CarDeductPointBase(BaseModel):
    total: int


class CarDeductPoint(BaseModel):
    data: CarDeductPointBase
    pager: Optional[Pager] = None


### product ###
class ProductBase(BaseModel):
    id: int
    name: str
    stock: int
    point: int
    is_launched: bool


class Product(BaseModel):
    data: List[ProductBase]
    pager: Optional[Pager] = None


### qrcode ###
class DecodeProductBase(BaseModel):
    id: int
    name: str
    user_id: int
    point: int


class DecodeProduct(BaseModel):
    data: DecodeProductBase
    pager: Optional[Pager] = None


class EncodeProductBase(BaseModel):
    image: str


class EncodeProduct(BaseModel):
    data: EncodeProductBase
    pager: Optional[Pager] = None


### trip ###
class TripBase(BaseModel):
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


class Trip(BaseModel):
    data: List[TripBase]
    pager: Optional[Pager] = None


class ResponseHandler:
    @staticmethod
    def response(result, pager=None):
        if isinstance(result, bool):
            return {'success': result}
        else:
            return {'data': result, 'pager': pager}
