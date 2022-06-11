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

from utils.const_template import ConstTemplate


class Const:
    class Role:
        GENERAL = 1  # 一般車主
        CHARGER_OWNER = 2  # 超充站長

    class Sex(ConstTemplate):
        MALE = '1'
        FEMALE = '2'

    class PointLogType:
        CREATE_TRIP = 1  # 新增旅程
        TRIP_LIKED = 2  # 被評分
        TRIP_DISLIKE = 3  # 被評分
        RATE_TRIP = 4  # 評分他人
        DELETE_CAR = 5  # 刪除車輛
        REDEEM_PRODUCT = 6  # 兌換
