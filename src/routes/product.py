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

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.product_handler import ProductHandler
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import general_auth, charger_owner_auth
from utils.payload_schemas import CreateProduct, UpdateProduct
from utils.response_models import Response, ResponseHandler

router = APIRouter(prefix='/products', tags=['product'])


@router.get('/{product_id}', response_model=Response[response_models.Product])
@router.get('', response_model=Response[response_models.Product])
async def get_product(product_id: int = None,
                      is_self: Optional[bool] = None,
                      charger_id: Optional[int] = None,
                      name: Optional[str] = None,
                      page: Optional[int] = 1,
                      per_page: Optional[int] = 10,
                      user: dict = Depends(general_auth),
                      db: Session = Depends(DBHandler.get_db)):
    result, pager = await ProductHandler.get_products(
        db=db,
        product_id=product_id,
        is_self=is_self,
        charger_id=charger_id,
        name=name,
        user=user,
        page=page,
        per_page=per_page
    )
    return ResponseHandler.response(result=result, pager=pager)


@router.post('', response_model=Response[response_models.Product])
async def create_product(product: CreateProduct, user: dict = Depends(charger_owner_auth),
                         db: Session = Depends(DBHandler.get_db)):
    result = await ProductHandler.create_product(
        db=db,
        user=user,
        name=product.name,
        stock=product.stock,
        point=product.point,
        is_launched=product.is_launched
    )
    return ResponseHandler.response(result=result)


@router.put('/{product_id}', response_model=Response[response_models.Product])
def update_product(product_id: int, product: UpdateProduct, user: dict = Depends(charger_owner_auth),
                   db: Session = Depends(DBHandler.get_db)):
    result = ProductHandler.update_product(
        db=db,
        user=user,
        product_id=product_id,
        name=product.name,
        stock=product.stock,
        point=product.point,
        is_launched=product.is_launched
    )
    return ResponseHandler.response(result=result)


@router.delete('/{product_id}', response_model=response_models.SuccessOrNot)
def delete_product(product_id: int, user: dict = Depends(charger_owner_auth), db: Session = Depends(DBHandler.get_db)):
    result = ProductHandler.delete_product(
        db=db,
        user=user,
        product_id=product_id
    )
    return ResponseHandler.response(result=result)


@router.post('/redeem-product/{token}', response_model=response_models.SuccessOrNot)
def redeem_product(token: str, user: dict = Depends(charger_owner_auth), db: Session = Depends(DBHandler.get_db)):
    result = ProductHandler.redeem_product(
        db=db,
        user=user,
        token=token
    )
    return ResponseHandler.response(result=result)
