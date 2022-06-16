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


class CarModelHandler:

    @classmethod
    async def get_car_models(cls, db: Session):
        car_models = DBHandler.get_car_models(db=db).all()
        results = list()
        for car_model in car_models:
            result = {
                'id': car_model.id,
                'model': car_model.model,
                'spec': car_model.spec,
            }
            results.append(result)
        return results
