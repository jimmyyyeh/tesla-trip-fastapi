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

from sqlalchemy import Column, Integer, ForeignKey, String, Float, Date, func, text, DateTime, Boolean

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    使用者
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    role = Column(Integer, nullable=False, server_default=text('1'), comment='角色')
    username = Column(String(30), nullable=False, unique=True, comment='帳號')
    password = Column(String(100), nullable=False, comment='密碼')
    nickname = Column(String(30), nullable=False, comment='暱稱')
    email = Column(String(100), nullable=False, comment='電子郵件')
    birthday = Column(Date, nullable=False, comment='生日')
    sex = Column(Integer, nullable=False, comment='性別')
    charger_id = Column(Integer, ForeignKey('super_charger.id'), comment='管理超充 id')
    is_verified = Column(Boolean, nullable=False, server_default=text('0'), comment='是否已驗證')
    point = Column(Integer, nullable=False, server_default=text('0'), comment='積分')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class PointLog(Base):
    """
    使用者
    """
    __tablename__ = 'point_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='使用者 id')
    type = Column(Integer, nullable=False, comment='分類')
    point = Column(Integer, nullable=False, comment='點數快照')
    change = Column(Integer, nullable=False, comment='增減數')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class Car(Base):
    """
    車輛資料
    """
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='使用者 id')
    car_model_id = Column(Integer, ForeignKey('car_model.id'), nullable=False, comment='車種型號 id')
    manufacture_date = Column(Date, nullable=False, comment='出廠日期')
    has_image = Column(Boolean, nullable=False, server_default=text('0'), comment='是否擁有圖片')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class CarModel(Base):
    """
    車種型號
    """
    __tablename__ = 'car_model'
    id = Column(Integer, primary_key=True)
    model = Column(String(10), nullable=False, comment='型號')
    spec = Column(String(30), nullable=False, comment='規格')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class AdministrativeDistrict(Base):
    """
    行政區列表
    """
    __tablename__ = 'administrative_district'
    id = Column(Integer, primary_key=True)
    city = Column(String(10), nullable=False, comment='縣市')
    area = Column(String(10), nullable=False, comment='區域')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class SuperCharger(Base):
    """
    超充站列表
    """
    __tablename__ = 'super_charger'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, comment='名稱')
    city = Column(String(10), nullable=False, comment='縣市')
    tpc = Column(Integer, comment='tpc數量')
    ccs2 = Column(Integer, comment='ccs2數量')
    floor = Column(String(10), comment='樓層')
    business_hours = Column(String(30), comment='營業時間')
    park_fee = Column(String(10), comment='停車費率')
    charger_fee = Column(String(10), comment='充電費率')
    version = Column(String(10), comment='版本')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class Trip(Base):
    """
    旅程
    """
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='使用者 id')
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False, comment='車輛 id')
    mileage = Column(Integer, comment='滿電里程')
    consumption = Column(Float, comment='平均電力')
    total = Column(Float, comment='電量總計')
    start = Column(String(30), nullable=False, comment='起點')
    end = Column(String(30), nullable=False, comment='終點')
    start_battery_level = Column(Integer, comment='起點電量')
    end_battery_level = Column(Integer, comment='終點電量')
    is_charge = Column(Boolean, server_default=text('0'), comment='是否充電')
    charger_id = Column(Integer, ForeignKey('super_charger.id'), comment='超充站 id')
    charge = Column(Integer, comment='充電%數')
    fee = Column(Integer, comment='充電費用')
    trip_date = Column(Date, nullable=False, comment='旅程日期')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class TripRate(Base):
    """
    旅程評分
    """
    __tablename__ = 'trip_rate'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='使用者 id')
    trip_id = Column(Integer, ForeignKey('trip.id'), nullable=False, comment='旅程 id')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class Product(Base):
    """
    產品
    """
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, comment='名稱')
    point = Column(Integer, nullable=False, comment='點數')
    stock = Column(Integer, nullable=False, comment='庫存')
    charger_id = Column(Integer, ForeignKey('super_charger.id'), nullable=False, comment='超充站 id')
    is_launched = Column(Boolean, nullable=False, server_default=text('0'), comment='是否上架')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')


class RedeemLog(Base):
    """
    兌換紀錄
    """
    __tablename__ = 'redeem_log'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='賣方 id')
    buyer_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='買方 id')
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False, comment='產品 id')

    create_datetime = Column(DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                             comment='更新時間')
