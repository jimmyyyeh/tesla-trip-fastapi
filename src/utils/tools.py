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

import math
from datetime import datetime, date


class Tools:
    @staticmethod
    def make_pager(db, page, per_page, model):
        total = db.query(model.id).count()
        return {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': math.ceil(total / per_page),
        }

    @staticmethod
    def serialize_result(dict_):
        for key, value in dict_.items():
            if isinstance(value, datetime):
                dict_[key] = value.strftime('%F %X')
            elif isinstance(value, date):
                dict_[key] = value.strftime('%F')

    @staticmethod
    def date_to_season(date_):
        year = date_.year
        month = date_.month
        season = int(month % 3.1 + 1)
        return f'{year}Q{season}'

    @staticmethod
    def get_deduct_point(trips, trip_rates):
        return trips.count() + trip_rates.count() * 2
