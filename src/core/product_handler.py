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

from typing import Optional

from sqlalchemy.orm import Session

from database.db_handler import DBHandler
from database.models import Product
from database.redis_handler import RedisHandler
from utils.const import Const
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundException, ValidationException
from utils.tools import Tools


class ProductHandler:
    @staticmethod
    async def get_products(db: Session, product_id: int, is_self: bool, charger_id: int, name: str, user: dict,
                           page: int, per_page: int):
        products = DBHandler.get_products(
            db=db,
            product_id=product_id,
            is_self=is_self,
            charger_id=charger_id,
            name=name,
            user=user,
            page=page,
            per_page=per_page
        )
        pager = Tools.make_pager(
            db=db,
            page=page,
            per_page=per_page,
            model=Product
        )

        results = list()
        for product in products:
            result = {
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'point': product.point,
                'is_launched': product.is_launched
            }
            results.append(result)
        return results, pager

    @staticmethod
    async def create_product(db: Session, user: dict, name: str, stock: int, point: int,
                             is_launched: Optional[bool] = False):
        product = DBHandler.create_product(
            db=db,
            user=user,
            name=name,
            stock=stock,
            point=point,
            is_launched=is_launched
        )
        result = {
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'point': product.point,
            'is_launched': product.is_launched
        }
        return result

    @classmethod
    async def update_product(cls, db: Session, user: dict, product_id: int, name: Optional[str] = None,
                             stock: Optional[int] = None, point: Optional[int] = None,
                             is_launched: Optional[bool] = False):
        product = DBHandler.update_product(
            db=db,
            product_id=product_id,
            user=user,
            name=name,
            stock=stock,
            point=point,
            is_launched=is_launched
        )
        result = {
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'point': product.point,
            'is_launched': product.is_launched
        }
        return result

    @classmethod
    async def delete_product(cls, db: Session, user: dict, product_id: int):
        DBHandler.delete_product(db=db, user=user, product_id=product_id)
        return True

    @classmethod
    async def redeem_product(cls, db: Session, user: dict, token: str):
        content = RedisHandler.get_redeem_product(token=token)
        if not content:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        buyer_id = content['user_id']
        product_id = content['id']
        product = DBHandler.get_product(
            db=db,
            product_id=product_id
        ).first()
        if not product:
            raise NotFoundException(
                error_msg='data not found',
                error_code=ErrorCodes.DATA_NOT_FOUND
            )
        if product.stock == 0:
            raise ValidationException(
                error_msg='insufficient product stock',
                error_code=ErrorCodes.INSUFFICIENT_PRODUCT_STOCK
            )
        product.stock -= 1
        product_point = content['point']
        seller = user
        buyer = DBHandler.get_user_by_id(
            db=db,
            id_=buyer_id
        )

        origin_point = buyer.point
        if origin_point < product_point:
            raise ValidationException(
                error_msg='insufficient point',
                error_code=ErrorCodes.INSUFFICIENT_POINT
            )
        buyer.point -= product_point
        DBHandler.create_redeem_log(db=db, seller_id=seller['id'], buyer_id=buyer_id, product_id=product_id)
        DBHandler.create_point_log(
            db=db,
            user_id=buyer.id,
            point=origin_point,
            change=product_point,
            type_=Const.PointLogType.REDEEM_PRODUCT
        )
        db.commit()
        RedisHandler.delete_redeem_product(token=token)
        return True
