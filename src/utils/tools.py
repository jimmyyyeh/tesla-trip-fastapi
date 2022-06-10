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

from datetime import datetime, date


class Tools:
    @staticmethod
    def make_pager(page, per_page, objs):
        return {
            'page': page,
            'per_page': per_page,
            'total': objs.total,
            'pages': objs.pages,
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
