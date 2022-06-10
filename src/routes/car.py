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

from fastapi import APIRouter
from utils.payload_schema import CreateCar, UpdateCar

router = APIRouter(prefix='/car', tags=['car'])


@router.get('/{car_id}')
@router.get('/')
def get_car(car_id: int = None):
    ...


@router.post('/')
def create_car(car_info: CreateCar):
    return ''


@router.put('/{car_id}')
def update_car(car_id: int, car_info: UpdateCar):
    return ''


@router.delete('/{car_id}')
def delete_car(car_id: int):
    ...


@router.get('/car-model')
def get_car_model():
    ...


@router.get('/deduct-point/{car_id}')
def get_car_deduct_point(car_id: int):
    ...
