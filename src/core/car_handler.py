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
import base64
from datetime import date
from pathlib import Path
from typing import List

from sqlalchemy.orm import Session

from database.db_handler import DBHandler
from database.models import Trip, TripRate, User
from utils.const import Const
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundException
from utils.pattern import Pattern
from utils.tools import Tools


class CarHandler:

    @classmethod
    async def get_cars(cls, db: Session, user_id: int, car_id: int):
        cars = DBHandler.get_cars(db=db, user_id=user_id, car_id=car_id).all()
        if not cars:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        results = list()
        for car in cars:
            result = {
                'id': car.id,
                'car': f'{car.model}-{car.spec}({Tools.date_to_season(car.manufacture_date)})',
                'model': car.model,
                'spec': car.spec,
                'manufacture_date': car.manufacture_date,
                'has_image': car.has_image
            }
            Tools.serialize_result(dict_=result)
            results.append(result)
        return results

    @staticmethod
    def _save_file(id_: int, file: str):
        if not file:
            return None
        _, extension, _, base64_str = Pattern.BASE64.search(file).groups()
        path = './static/image/car'
        filename = f'{id_}.jpg'
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(f'{path}/{filename}', 'wb') as f:
            f.write(base64.decodebytes(base64_str.encode()))
        return filename

    @classmethod
    async def create_car(cls, db: Session, user_id: int, model: str, spec: str, manufacture_date: date, file: str):
        car_model = DBHandler.get_car_models(db=db, model=model, spec=spec).first()

        if not car_model:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        car = DBHandler.create_car(
            db=db,
            user_id=user_id,
            car_model_id=car_model.id,
            manufacture_date=manufacture_date,
            file=file
        )
        cls._save_file(file=file, id_=car.id)
        db.commit()
        result = {
            'id': car.id,
            'car': f'{car_model.model}-{car_model.spec}({Tools.date_to_season(car.manufacture_date)})',
            'model': car_model.model,
            'spec': car_model.spec,
            'manufacture_date': car.manufacture_date,
            'has_image': car.has_image
        }
        return result

    @classmethod
    async def update_car(cls, db: Session, user_id: int, car_id: int, model: str, spec: str, manufacture_date: date):
        car = DBHandler.get_car(db=db, user_id=user_id, car_id=car_id).first()
        if not car:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        car_model = DBHandler.get_car_models(db=db, model=model, spec=spec).first()
        if not car_model:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )

        car.car_model_id = car_model.id
        car.manufacture_date = manufacture_date
        db.add(car)
        db.commit()
        result = {
            'id': car.id,
            'car': f'{car_model.model}-{car_model.spec}({Tools.date_to_season(car.manufacture_date)})',
            'model': car_model.model,
            'spec': car_model.spec,
            'manufacture_date': car.manufacture_date,
            'has_image': car.has_image
        }
        return result

    @staticmethod
    def _deduct_point(db: Session, user: User, trips: List[Trip], trip_rates: List[TripRate]):
        origin_point = user.point
        total_deduct = Tools.get_deduct_point(trips=trips, trip_rates=trip_rates)
        if origin_point < total_deduct:
            user.point = 0
            deduct_point = origin_point
        else:
            user.point -= total_deduct
            deduct_point = user.point
        DBHandler.create_point_log(
            db=db,
            user_id=user.id,
            point=origin_point,
            change=deduct_point,
            type_=Const.PointLogType.DELETE_CAR,
        )

    @classmethod
    def _get_delete_car_info(cls, db: Session, user_id: int, car_id: int):
        trips = DBHandler.get_user_trips(db=db, car_id=car_id)
        trip_ids = {trip.id for trip in trips}
        trip_rates = DBHandler.get_trip_rates(db=db, trip_ids=trip_ids)
        car = DBHandler.get_car(db=db, user_id=user_id, car_id=car_id)
        return car, trips, trip_rates

    @classmethod
    async def delete_car(cls, db: Session, user: dict, car_id: id):
        car, trips, trip_rates = cls._get_delete_car_info(db=db, user_id=user['id'], car_id=car_id)
        if trip_rates:
            trip_rates.delete()
        if trips:
            trips.delete()
        car.delete()
        user = DBHandler.get_user_by_id(db=db, id_=user['id'])
        cls._deduct_point(db=db, user=user, trips=trips, trip_rates=trip_rates)
        db.commit()
        return True

    @classmethod
    async def get_car_deduct_point(cls, db: Session, user: dict, car_id: int):
        _, trips, trip_rates = cls._get_delete_car_info(db=db, user_id=user['id'], car_id=car_id)
        total_deduct = Tools.get_deduct_point(trips=trips, trip_rates=trip_rates)
        return {'total': total_deduct}
