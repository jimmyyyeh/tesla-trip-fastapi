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
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator
from utils.payload_schemas import UpdateTripRate
from utils.response_models import Response, ResponseHandler

router = APIRouter(prefix='/trip-rates', tags=['trip rate'])
general_auth = AuthValidator()


@router.put('/', response_model=response_models.SuccessOrNot)
async def update_trip_rate(payload: UpdateTripRate, user: dict = Depends(general_auth),
                           db: Session = Depends(DBHandler.get_db)):
    result = await TripRateHandler.update_user_trip_rate(
        db=db,
        user=user,
        trip_id=payload.trip_id
    )
    return ResponseHandler.response(result=result)
