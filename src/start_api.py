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

import uvicorn

from app import create_app
from routes import *

app = create_app()

app.include_router(user.router)
app.include_router(administrative_district.router)
app.include_router(car.router)
app.include_router(car_model.router)
app.include_router(charger.router)
app.include_router(trip.router)
app.include_router(trip_rate.router)
app.include_router(product.router)
app.include_router(qrcode.router)
app.include_router(event.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
