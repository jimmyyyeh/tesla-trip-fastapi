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
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator
from utils.payload_schemas import EncodeProduct
from utils.response_models import ResponseHandler

router = APIRouter(prefix='/qrcode', tags=['qrcode'])
general_auth = AuthValidator()

@router.get('/product/{token}', response_model=response_models.DecodeProduct)
def decode_product(token: str, user: dict = Depends(general_auth)):
    result = QRCodeHandler.decode_product(
        token=token
    )
    return ResponseHandler.response(result=result)


@router.post('/product', response_model=response_models.EncodeProduct)
def encode_product(payload: EncodeProduct, user: dict = Depends(general_auth),
                   db: Session = Depends(DBHandler.get_db)):
    result = QRCodeHandler.encode_product(
        db=db,
        user=user,
        product_id=payload.product_id
    )
    return ResponseHandler.response(result=result)
