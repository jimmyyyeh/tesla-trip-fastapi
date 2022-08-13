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
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.charger_handler import ChargerHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import general_auth
from utils.response_models import Response, ResponseHandler

router = APIRouter(prefix='/super-chargers', tags=['super charger'])


@router.get('', response_model=Response[List[response_models.SuperCharger]])
async def get_super_charger(user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = await ChargerHandler.get_chargers(db=db)
    return ResponseHandler.response(result=result)
