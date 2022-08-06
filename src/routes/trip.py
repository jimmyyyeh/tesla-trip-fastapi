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

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.trip_handler import TripHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator
from utils.payload_schemas import CreateTrip
from utils.response_models import Response, ResponseHandler

router = APIRouter(prefix='/trips', tags=['trip'])
general_auth = AuthValidator()


@router.get('/', response_model=Response[response_models.Trip])
async def get_trip(is_my_trip: Optional[bool] = None, page: Optional[int] = 1, per_page: Optional[int] = 10,
                   charger: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None,
                   model: Optional[str] = None, spec: Optional[str] = None, user: dict = Depends(general_auth),
                   db: Session = Depends(DBHandler.get_db)):
    result, pager = await TripHandler.get_trips(
        db=db,
        user_id=user['id'],
        is_my_trip=is_my_trip,
        charger=charger,
        start=start,
        end=end,
        model=model,
        spec=spec,
        page=page,
        per_page=per_page
    )
    return ResponseHandler.response(result=result, pager=pager)


@router.post('/', response_model=response_models.SuccessOrNot)
async def create_trip(trips: List[CreateTrip], user: dict = Depends(general_auth),
                      db: Session = Depends(DBHandler.get_db)):
    result = await TripHandler.create_trip(
        db=db,
        user_id=user['id'],
        trips=trips
    )
    return ResponseHandler.response(result=result)
