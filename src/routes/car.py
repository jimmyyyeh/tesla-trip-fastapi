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

from core.car_handler import CarHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator
from utils.payload_schemas import CreateCar, UpdateCar
from utils.response_models import ResponseHandler

router = APIRouter(prefix='/car', tags=['car'])
general_auth = AuthValidator()


@router.get('/car-model', response_model=response_models.CarModel)
def get_car_model(user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = CarHandler.get_car_models(
        db=db
    )
    return ResponseHandler.response(result=result)


@router.get('/{car_id}', response_model=response_models.Car)
@router.get('/', response_model=response_models.Car)
def get_car(car_id: int = None, user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = CarHandler.get_cars(db=db, user_id=user['id'], car_id=car_id)
    return ResponseHandler.response(result=result)


@router.post('/', response_model=response_models.Car)
def create_car(car_info: CreateCar, user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = CarHandler.create_car(
        db=db,
        user_id=user['id'],
        model=car_info.model,
        spec=car_info.spec,
        manufacture_date=car_info.manufacture_date,
        file=car_info.file
    )
    return ResponseHandler.response(result=result)


@router.put('/{car_id}', response_model=response_models.Car)
def update_car(car_id: int, car_info: UpdateCar, user: dict = Depends(general_auth),
               db: Session = Depends(DBHandler.get_db)):
    result = CarHandler.update_car(
        db=db,
        user_id=user['id'],
        car_id=car_id,
        model=car_info.model,
        spec=car_info.spec,
        manufacture_date=car_info.manufacture_date
    )
    return ResponseHandler.response(result=result)


@router.delete('/{car_id}', response_model=response_models.SuccessOrNot)
def delete_car(car_id: int, user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = CarHandler.delete_car(
        db=db,
        user=user,
        car_id=car_id
    )
    return ResponseHandler.response(result=result)


@router.get('/deduct-point/{car_id}', response_model=response_models.CarDeductPoint)
def get_car_deduct_point(car_id: int, user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = CarHandler.get_car_deduct_point(db=db, user=user, car_id=car_id)
    return ResponseHandler.response(result=result)
