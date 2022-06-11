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

from database.crud import CRUD
from database.models import User
from utils.const import Const


class TripRateHandler:

    @staticmethod
    def _rise_user_point(db: Session, user: User, trip_author: User):
        user_origin_point = user.point
        author_origin_point = trip_author.point
        trip_author.point += 1
        CRUD.create_point_log(
            db=db,
            user_id=trip_author.id,
            point=author_origin_point,
            type_=Const.PointLogType.TRIP_LIKED,
            change=1
        )
        if user != trip_author:
            user.point += 1
            CRUD.create_point_log(
                db=db,
                user_id=user.id,
                point=user_origin_point,
                type_=Const.PointLogType.RATE_TRIP,
                change=1
            )

    @staticmethod
    def _deduct_user_point(db: Session, trip_author: User):
        author_origin_point = trip_author.point
        trip_author.point -= 1
        CRUD.create_point_log(
            db=db,
            user_id=trip_author.id,
            point=author_origin_point,
            type_=Const.PointLogType.TRIP_DISLIKE,
            change=1
        )

    @classmethod
    def update_user_trip_rate(cls, db: Session, user: dict, trip_id: int):
        trip = CRUD.get_trip(db=db, trip_id=trip_id)

        if not trip:
            # TODO raise
            ...
        trip_rater = CRUD.get_user_by_id(db=db, id_=user['id'])
        trip_author = CRUD.get_user_by_id(db=db, id_=trip.user_id)
        trip_rate = CRUD.get_trip_rate(db=db, user_id=trip_author.id, trip_id=trip_id)
        if not trip_rate.first():
            CRUD.create_trip_rate(db=db, user_id=user['id'], trip_id=trip_id)
            cls._rise_user_point(db=db, user=trip_rater, trip_author=trip_author)
        else:
            trip_rate.delete()
            cls._deduct_user_point(db=db, trip_author=trip_author)

        db.commit()
        return True
