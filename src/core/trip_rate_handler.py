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
from sqlalchemy.orm import Session

from database.db_handler import DBHandler
from database.models import User
from utils.const import Const
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundException


class TripRateHandler:

    @staticmethod
    def _rise_user_point(db: Session, user: User, trip_author: User):
        user_origin_point = user.point
        author_origin_point = trip_author.point
        trip_author.point += 1
        DBHandler.create_point_log(
            db=db,
            user_id=trip_author.id,
            point=author_origin_point,
            type_=Const.PointLogType.TRIP_LIKED,
            change=1
        )
        if user != trip_author:
            user.point += 1
            DBHandler.create_point_log(
                db=db,
                user_id=user.id,
                point=user_origin_point,
                type_=Const.PointLogType.RATE_TRIP,
                change=1
            )

    @staticmethod
    def _deduct_user_point(db: Session, user: User, trip_author: User):
        user_origin_point = user.point
        author_origin_point = trip_author.point
        trip_author.point -= 1
        DBHandler.create_point_log(
            db=db,
            user_id=trip_author.id,
            point=author_origin_point,
            type_=Const.PointLogType.TRIP_DISLIKE,
            change=1
        )

        if user != trip_author:
            user.point -= 1
            DBHandler.create_point_log(
                db=db,
                user_id=user.id,
                point=user_origin_point,
                type_=Const.PointLogType.DELETE_RATE_TRIP,
                change=1
            )

    @classmethod
    async def update_user_trip_rate(cls, db: Session, user: dict, trip_id: int):
        trip = DBHandler.get_trip(db=db, trip_id=trip_id)

        if not trip:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        trip_rater = DBHandler.get_user_by_id(db=db, id_=user['id'])
        trip_author = DBHandler.get_user_by_id(db=db, id_=trip.user_id)
        trip_rate = DBHandler.get_trip_rate(db=db, user_id=trip_author.id, trip_id=trip_id)
        if not trip_rate.first():
            DBHandler.create_trip_rate(db=db, user_id=user['id'], trip_id=trip_id)
            cls._rise_user_point(db=db, user=trip_rater, trip_author=trip_author)
        else:
            trip_rate.delete()
            cls._deduct_user_point(db=db, user=trip_rater, trip_author=trip_author)

        db.commit()
        return True
