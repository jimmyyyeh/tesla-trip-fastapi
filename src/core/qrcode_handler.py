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
from io import BytesIO
from secrets import token_hex

import qrcode
from sqlalchemy.orm import Session

from app import settings
from database.db_handler import DBHandler
from database.redis_handler import RedisHandler
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundException


class QRCodeHandler:
    @staticmethod
    async def decode_product(token: str):
        content = RedisHandler.get_redeem_product(token=token)
        if not content:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        return content

    @staticmethod
    async def encode_product(db: Session, user: dict, product_id: int):
        product = DBHandler.get_product(db=db, product_id=product_id).first()
        if not product:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        content = {
            'user_id': user['id'],
            'id': product.id,
            'name': product.name,
            'point': product.point
        }
        token = token_hex(16)
        RedisHandler.set_redeem_product(token=token, content=content)

        url = f'{settings.web_domain}/redeem/{token}'
        qrcode_ = qrcode.make(url)
        img = BytesIO()
        qrcode_.save(img, format='PNG')
        img = img.getvalue()
        result = {
            'image': base64.b64encode(img).decode()
        }
        return result
