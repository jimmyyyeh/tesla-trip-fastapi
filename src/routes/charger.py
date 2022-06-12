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
from utils.auth_tools import AuthValidator

router = APIRouter(prefix='/super-charger', tags=['super charger'])
general_auth = AuthValidator()

@router.get('/', response_model=List[response_models.SuperCharger])
def get_super_charger(user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = ChargerHandler.get_chargers(db=db)
    return result
