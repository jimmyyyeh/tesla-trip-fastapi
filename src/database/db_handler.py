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
from datetime import date, datetime, timedelta
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from database.db_manager import SessionLocal
from database.models import User, AdministrativeDistrict, SuperCharger, Car, CarModel, PointLog, Trip, TripRate, \
    Product, RedeemLog
from utils.auth_tools import AuthTools
from utils.const import Const


class DBHandler:
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    ### user ###
    @staticmethod
    def get_user_by_id(db: Session, id_: int):
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
    def get_car_models(db: Session, model: Optional[str] = None, spec: Optional[str] = None):
        filter_ = list()
        if model:
            filter_.append(CarModel.model == model)
        if spec:
            filter_.append(CarModel.spec == spec)
        car_models = db.query(CarModel).filter(
            *filter_
        )
        return car_models

    ### log ###

    @staticmethod
    def create_point_log(db: Session, user_id: int, point: int, change: int, type_: int):
        point_log = PointLog(
            user_id=user_id,
            point=point,
            change=change,
            type=type_
        )
        db.add(point_log)

    @staticmethod
    def create_redeem_log(db: Session, seller_id: int, buyer_id: int, product_id: int):
        redeem_log = RedeemLog(
            seller_id=seller_id,
            buyer_id=buyer_id,
            product_id=product_id,
        )
        db.add(redeem_log)

    ### trip ###
    @staticmethod
    def get_user_trips(db: Session, car_id: int):
        trips = db.query(Trip).filter(
            Trip.car_id == car_id
        )
        return trips

    @staticmethod
    def get_trip(db: Session, trip_id: int):
        trip = db.query(Trip).filter(
            Trip.id == trip_id
        ).first()
        return trip

    @staticmethod
    def get_trips(db: Session, user_id: int, page: int, per_page: int, is_my_trip: Optional[bool] = None,
                  charger: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None,
                  model: Optional[str] = None, spec: Optional[str] = None):
        now_ = datetime.now()
        filter_ = [
            Trip.create_datetime >= now_ - timedelta(days=365),
        ]
        # 限制近一年 避免資料太多
        if is_my_trip:
            filter_.append(Trip.user_id == user_id)
        if charger:
            filter_.append(SuperCharger.id == charger)
        if start:
            filter_.append(Trip.start.like(f'%{start}%'))
        if end:
            filter_.append(Trip.end.like(f'%{end}%'))
        if model:
            filter_.append(CarModel.model.like(f'%{model}%'))
        if spec:
            filter_.append(CarModel.spec.like(f'%{spec}%'))

        trip_rate_count = db.query(
            TripRate.trip_id.label('trip_id'),
            func.count(TripRate.trip_id).label('trip_rate_count')
        ).group_by(
            TripRate.trip_id
        ).subquery()

        is_rate = db.query(
            TripRate.id.label('is_rate'),
            TripRate.trip_id.label('trip_id')
        ).filter(
            TripRate.user_id == user_id
        ).subquery()

        trips = db.query(
            Trip.id,
            Trip.mileage,
            Trip.consumption,
            Trip.total,
            Trip.start,
            Trip.start_battery_level,
            Trip.end,
            Trip.end_battery_level,
            Trip.is_charge,
            Trip.charge,
            Trip.fee,
            Trip.trip_date,
            trip_rate_count.c.trip_rate_count,
            is_rate.c.is_rate,
            CarModel.model,
            CarModel.spec,
            Car.manufacture_date,
            SuperCharger.name,
        ).outerjoin(
            Car, Car.id == Trip.car_id
        ).join(
            CarModel, CarModel.id == Car.car_model_id,
        ).outerjoin(
            SuperCharger, SuperCharger.id == Trip.charger_id
        ).outerjoin(
            trip_rate_count, trip_rate_count.c.trip_id == Trip.id
        ).outerjoin(
            is_rate, is_rate.c.trip_id == Trip.id
        ).filter(
            *filter_
        ).order_by(
            Trip.create_datetime.desc()
        ).limit(
            per_page
        ).offset(
            (page - 1) * per_page
        ).all()
        return trips

    @classmethod
    def create_trip(cls, db: Session, user_id: int, car_id: int, mileage: int, consumption: float, total: float,
                    start: str,
                    end: str, start_battery_level: int, end_battery_level: int, is_charge: bool, trip_date: date,
                    charger_id: Optional[int] = None, charge: Optional[int] = None, fee: Optional[int] = None):
        trip_ = Trip(
            user_id=user_id,
            car_id=car_id,
            mileage=mileage,
            consumption=consumption,
            total=total,
            start=start,
            end=end,
            start_battery_level=start_battery_level,
            end_battery_level=end_battery_level,
            is_charge=is_charge,
            charger_id=charger_id,
            charge=charge,
            fee=fee,
            trip_date=trip_date,
        )
        db.add(trip_)
        user = cls.get_user_by_id(db=db, id_=user_id)
        origin_point = user.point
        user.point += 1
        cls.create_point_log(
            db=db,
            user_id=user.id,
            point=origin_point,
            type_=Const.PointLogType.CREATE_TRIP,
            change=1
        )

    @staticmethod
    def get_trip_rate(db: Session, user_id: int, trip_id: int):
        filter_ = [
            TripRate.trip_id == trip_id,
            TripRate.user_id == user_id
        ]
        trip_rate = db.query(TripRate).filter(
            *filter_
        )
        return trip_rate

    @staticmethod
    def create_trip_rate(db: Session, user_id=int, trip_id=int):
        trip_rate = TripRate(
            user_id=user_id,
            trip_id=trip_id
        )
        db.add(trip_rate)
        return trip_rate

    @staticmethod
    def get_trip_rates(db: Session, trip_ids=set):
        trip_rates = db.query(TripRate).filter(
            TripRate.trip_id.in_(trip_ids)
        )
        return trip_rates

    ### product ###
    @staticmethod
    def get_product(db: Session, product_id: int, charger_id: Optional[int] = None):
        filter_ = [Product.id == product_id]
        if charger_id:
            filter_.append(Product.charger_id == charger_id)
        product = db.query(Product).filter(
            *filter_
        )
        return product

    @staticmethod
    def get_products(db: Session, product_id: int, is_self: bool, charger_id: int, name: str, user: dict, page: int,
                     per_page: int):
        filter_ = []
        if product_id:
            filter_.append(Product.id == product_id)
        if is_self:
            filter_.append(SuperCharger.id == user['charger_id'])
        if charger_id:
            filter_.append(SuperCharger.id == charger_id)
        if name:
            filter_.append(Product.name.like(f'%{name}%'))
        products = db.query(
            Product.id,
            Product.name,
            Product.stock,
            Product.point,
            Product.is_launched,
            SuperCharger.name.label('charger')
        ).join(
            SuperCharger, SuperCharger.id == Product.charger_id
        ).filter(
            *filter_
        ).limit(
            per_page
        ).offset(
            (page - 1) * per_page
        ).all()
        return products

    @staticmethod
    def create_product(db: Session, user: dict, name: str, stock: int, point: int, is_launched: bool = False):
        product = Product(
            name=name,
            stock=stock,
            point=point,
            is_launched=is_launched,
            charger_id=user['charger_id'],
        )
        db.add(product)
        db.commit()
        return product

    @classmethod
    def update_product(cls, db: Session, product_id: int, user: dict, name: Optional[str] = None,
                       stock: Optional[int] = None, point: Optional[int] = None, is_launched: Optional[bool] = False):
        product = cls.get_product(db=db, product_id=product_id, charger_id=user['charger_id']).first()
        if not product:
            # TODO raise
            ...
        if name:
            product.name = name
        if stock:
            product.stock = stock
        if point:
            product.point = point
        if is_launched:
            product.is_launched = is_launched
        db.add(product)
        db.commit()
        return product

    @classmethod
    def delete_product(cls, db: Session, product_id: int, user: dict):
        product = cls.get_product(db=db, product_id=product_id, charger_id=user['charger_id'])
        if not product:
            # TODO raise
            ...
        product.delete()
        db.commit()
