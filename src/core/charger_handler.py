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


class ChargerHandler:
    @staticmethod
    def get_chargers(db: Session):
        super_chargers = CRUD.get_chargers(db=db)
        results = list()
        for super_charger in super_chargers:
            result = {
                'id': super_charger.id,
                'name': super_charger.name,
                'city': super_charger.city,
                'tpc': super_charger.tpc,
                'ccs2': super_charger.ccs2,
                'floor': super_charger.floor,
                'business_hours': super_charger.business_hours,
                'park_fee': super_charger.park_fee,
                'charger_fee': super_charger.charger_fee,
                'version': super_charger.version
            }
            results.append(result)
        return results
