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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# from core.car_handler import CarHandler
from database.crud import CRUD
from utils.auth_tools import AuthTools
from utils.payload_schemas import CreateCar, UpdateCar

router = APIRouter(prefix='/car', tags=['car'])


@router.get('/{car_id}')
@router.get('/')
def get_car(car_id: int = None, user: dict = Depends(AuthTools.verify_auth),db: Session = Depends(CRUD.get_db)):
    # result = CarHandler.get_cars(db=db, user_id=user['id'], car_id=car_id)
    # return result
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
