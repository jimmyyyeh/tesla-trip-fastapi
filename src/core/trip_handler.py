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

from sqlalchemy.orm import Session

from database.db_handler import DBHandler
from database.models import Trip
from utils.payload_schemas import CreateTrip
from utils.tools import Tools


class TripHandler:
    @staticmethod
    def get_trips(db: Session, user_id: int, is_my_trip: bool, page: int, per_page: int, charger: str, start: str,
                  end: str, model: str, spec: str):
        trips = DBHandler.get_trips(
            db=db,
            user_id=user_id,
            is_my_trip=is_my_trip,
            charger=charger,
            start=start,
            end=end,
            model=model,
            spec=spec,
            page=page,
            per_page=per_page
        )
        pager = Tools.make_pager(
            db=db,
            page=page,
            per_page=per_page,
            model=Trip
        )
        results = list()
        for trip in trips:
            result = {
                'id': trip.id,
                'mileage': trip.mileage,
                'consumption': trip.consumption,
                'total': trip.total,
                'start': trip.start,
                'end': trip.end,
                'start_battery_level': trip.start_battery_level,
                'end_battery_level': trip.end_battery_level,
                'is_charge': trip.is_charge,
                'charge': trip.charge,
                'fee': trip.fee,
                'trip_date': trip.trip_date,
                'car': f'{trip.model}-{trip.spec}({Tools.date_to_season(trip.trip_date)})',
                'charger': trip.name,
                'trip_rate_count': trip.trip_rate_count,
                'is_rate': True if trip.is_rate else False
            }
            results.append(result)
        return results, pager

    @staticmethod
    def create_trip(db: Session, user_id: int, trips: List[CreateTrip]):
        for trip in trips:
            DBHandler.create_trip(
                db=db,
                user_id=user_id,
                car_id=trip.car_id,
                mileage=trip.mileage,
                consumption=trip.consumption,
                total=trip.total,
                start=trip.start,
                end=trip.end,
                start_battery_level=trip.start_battery_level,
                end_battery_level=trip.end_battery_level,
                is_charge=trip.is_charge,
                charger_id=trip.charger_id,
                charge=trip.charge,
                fee=trip.fee,
                trip_date=trip.trip_date
            )
        db.commit()
        return True
