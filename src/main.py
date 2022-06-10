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

from fastapi import FastAPI
from passlib.context import CryptContext


from routes import *

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

app = FastAPI()
app.include_router(user.router)
app.include_router(administrative_district.router)
app.include_router(car.router)
app.include_router(charger.router)
app.include_router(trip.router)
app.include_router(trip_rate.router)
app.include_router(product.router)
app.include_router(qrcode.router)
