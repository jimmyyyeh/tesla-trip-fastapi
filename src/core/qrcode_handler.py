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

import base64
import qrcode
from io import BytesIO
from secrets import token_hex

from sqlalchemy.orm import Session

from config import Config
from database.db_handler import DBHandler
from database.redis_handler import RedisHandler


class QRCodeHandler:
    @staticmethod
    def decode_product(token: str):
        content = RedisHandler.get_redeem_product(token=token)
        if not content:
            # TODO raise
            ...
        return content

    @staticmethod
    def encode_product(db: Session, user: dict, product_id: int):
        product = DBHandler.get_product(db=db, product_id=product_id).first()
        if not product:
            # TODO raise
            ...
        content = {
            'user_id': user['id'],
            'id': product.id,
            'name': product.name,
            'point': product.point
        }
        token = token_hex(16)
        RedisHandler.set_redeem_product(token=token, content=content)

        url = f'{Config.WEB_DOMAIN}/redeem/{token}'
        qrcode_ = qrcode.make(url)
        img = BytesIO()
        qrcode_.save(img, format='PNG')
        img = img.getvalue()
        result = {
            'image': base64.b64encode(img).decode()
        }
        return result
