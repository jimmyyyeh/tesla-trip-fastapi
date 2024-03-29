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

from core.administrative_district_handler import AdministrativeDistrictHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator
from utils.response_models import Response, ResponseHandler

router = APIRouter(prefix='/administrative-districts', tags=['administrative district'])
general_auth = AuthValidator()


@router.get('/', response_model=Response[response_models.AdministrativeDistrict])
async def get_administrative_district(user: dict = Depends(general_auth), db: Session = Depends(DBHandler.get_db)):
    result = await AdministrativeDistrictHandler.get_administrative_districts(db=db)
    return ResponseHandler.response(result=result)
