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

from core.trip_rate_handler import TripRateHandler
from database.crud import CRUD
from utils import response_models
from utils.auth_tools import AuthTools
from utils.payload_schemas import UpdateTripRate

router = APIRouter(prefix='/trip-rate', tags=['trip rate'])


@router.put('/', response_model=response_models.SuccessOrNot)
def update_trip_rate(payload: UpdateTripRate, user: dict = Depends(AuthTools.verify_auth),
                     db: Session = Depends(CRUD.get_db)):
    result = TripRateHandler.update_user_trip_rate(
        db=db,
        user=user,
        trip_id=payload.trip_id
    )
    return {'success': True}
