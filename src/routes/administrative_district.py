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
from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.administrative_district_handler import AdministrativeDistrictHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator

router = APIRouter(prefix='/administrative-district', tags=['administrative district'])
general_auth = AuthValidator()

@router.get('/', response_model=Dict[str, List[response_models.AdministrativeDistrict]])
def get_administrative_district(user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = AdministrativeDistrictHandler.get_administrative_districts(db=db)
    return result
