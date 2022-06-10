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

from fastapi import APIRouter
from utils.payload_schema import CreateProduct, UpdateProduct

router = APIRouter(prefix='/product', tags=['product'])


@router.get('/{product_id}')
@router.get('/')
def get_product(product_id: int = None):
    ...


@router.post('/')
def create_product(product: CreateProduct):
    ...


@router.put('/{product_id}')
def update_product(product_id: int, product: UpdateProduct):
    ...


@router.put('/{product_id}')
def delete_product(product_id: int):
    ...


@router.post('/redeem-product/{token}')
def redeem_product(token: str):
    ...
