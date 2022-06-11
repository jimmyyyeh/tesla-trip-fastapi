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
from database.crud import CRUD
from utils.auth_tools import AuthTools

router = APIRouter(prefix='/administrative-district', tags=['administrative district'])


@router.get('/')
def get_administrative_district(user: dict = Depends(AuthTools.verify_auth), db: Session = Depends(CRUD.get_db)):
    result = AdministrativeDistrictHandler.get_administrative_districts(db=db)
    return result
