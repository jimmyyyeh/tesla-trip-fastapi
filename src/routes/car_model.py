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

from core.car_model_handler import CarModelHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import general_auth
from utils.response_models import Response, ResponseHandler

router = APIRouter(prefix='/car-models', tags=['car'])


@router.get('/car-models', response_model=Response[response_models.CarModel])
async def get_car_model(user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = await CarModelHandler.get_car_models(
        db=db
    )
    return ResponseHandler.response(result=result)
