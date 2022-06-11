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
from datetime import date
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import User, AdministrativeDistrict, SuperCharger, Car, CarModel, PointLog, Trip, TripRate
from utils.auth_tools import AuthTools


class CRUD:
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    ### user ###
    @staticmethod
    def get_user_by_id(db: Session, id_: str):
        user = db.query(User).filter(User.id == id_).first()
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str, email: EmailStr = None):
        if email:
            conditions = [or_(User.username == username,
                              User.email == email)]
        else:
            conditions = [User.username == username]
        user = db.query(User).filter(*conditions).first()
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr):
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def create_user(db: Session, username: str, password: str, nickname: str, email: EmailStr, birthday: str, sex: int):
        user = User(
            username=username,
            password=AuthTools.get_password_hash(password=password),
            nickname=nickname,
            email=email,
            birthday=birthday,
            sex=sex
        )
        db.add(user)
        db.commit()
        # TODO send email
        return user

    ### administrative district  ###
    @staticmethod
    def get_administrative_district(db: Session):
        administrative_districts = db.query(AdministrativeDistrict).all()
        return administrative_districts

    ## super charger
    @staticmethod
    def get_chargers(db: Session):
        super_chargers = db.query(SuperCharger).all()
        return super_chargers

    ### car ###
    @staticmethod
    def get_car(db: Session, user_id: int, car_id: Optional[int] = None):
        car = db.query(Car).filter(
            Car.id == car_id,
            Car.user_id == user_id
        )
        return car

    @staticmethod
    def get_cars(db: Session, user_id: int, car_id: Optional[int] = None):
        filter_ = [
            Car.user_id == user_id,
        ]
        if car_id:
            filter_.append(Car.id == car_id)
        car = db.query(
            Car.id,
            Car.manufacture_date,
            Car.has_image,
            CarModel.model,
            CarModel.spec,
        ).join(
            CarModel, CarModel.id == Car.car_model_id
        ).filter(
            *filter_
        )
        if not car:
            # TODO raise
            ...
        return car

    @staticmethod
    def create_car(db: Session, user_id: int, car_model_id: int, manufacture_date: date, file: Optional[str] = None):
        car = Car(
            user_id=user_id,
            car_model_id=car_model_id,
            manufacture_date=manufacture_date,
            has_image=True if file else False
        )
        db.add(car)
        db.flush()
        return car

    @staticmethod
    def get_car_models(db:Session, model: Optional[str]=None, spec: Optional[str]=None):
        filter_ = list()
        if model:
            filter_.append(CarModel.model == model)
        if spec:
            filter_.append(CarModel.spec == spec)
        car_models = db.query(CarModel).filter(
            *filter_
        )
        return car_models

    ### point ###

    @staticmethod
    def create_point_log(db:Session, user_id: int, point: int, change:int, type_:int):
        point_log = PointLog(
            user_id=user_id,
            point=point,
            change=change,
            type=type_
        )
        db.add(point_log)
        db.commit()

    ### trip ###
    @staticmethod
    def get_trips(db:Session, car_id: int):
        trips = db.query(Trip).filter(
            Trip.car_id == car_id
        )
        return trips

    @staticmethod
    def get_trip_rates(db:Session, trip_ids=set):
        trip_rates = db.query(TripRate).filter(
            TripRate.trip_id.in_(trip_ids)
        )
        return trip_rates