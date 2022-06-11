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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.qrcode_handler import QRCodeHandler
from database.crud import CRUD
from utils import response_models
from utils.auth_tools import AuthTools
from utils.payload_schemas import EncodeProduct

router = APIRouter(prefix='/qrcode', tags=['qrcode'])


@router.get('/product/{token}', response_model=response_models.DecodeProduct)
def decode_product(token: str, user: dict = Depends(AuthTools.verify_auth)):
    result = QRCodeHandler.decode_product(
        token=token
    )
    return result


@router.post('/product', response_model=response_models.EncodeProduct)
def encode_product(payload: EncodeProduct, user: dict = Depends(AuthTools.verify_auth),
                   db: Session = Depends(CRUD.get_db)):
    result = QRCodeHandler.encode_product(
        db=db,
        user=user,
        product_id=payload.product_id
    )
    return result
