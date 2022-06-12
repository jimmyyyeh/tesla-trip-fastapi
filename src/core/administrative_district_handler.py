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


class AdministrativeDistrictHandler:
    @staticmethod
    def get_administrative_districts(db: Session):
        administrative_districts = DBHandler.get_administrative_district(
            db=db
        )
        results = dict()
        for administrative_district in administrative_districts:
            city = administrative_district.city
            if city not in results:
                results[city] = list()
            result = {
                'id': administrative_district.id,
                'area': administrative_district.area,
            }
            results[city].append(result)
        return results
