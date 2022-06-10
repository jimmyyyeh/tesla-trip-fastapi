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

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from core.user_handler import UserHandler
from database.crud import CRUD
from utils.payload_schemas import Verify, ResendVerify, SignIn, SignUp, UpdateProfile, RefreshToken, ResetPassword, \
    RequestResetPassword
from utils import response_models

router = APIRouter(tags=['user'])


@router.post('/verify')
def verify(payload: Verify):
    ...


@router.post('/resend-verify')
def resend_verify(payload: ResendVerify):
    ...


@router.post('/sign-in', response_model=response_models.SignIn)
def sign_in(payload: SignIn, db: Session = Depends(CRUD.get_db)):
    result = UserHandler.sign_in(
        db=db,
        payload=payload
    )
    return result


@router.post('/sign-up', response_model=response_models.SignUp)
async def sign_up(payload: SignUp, background_tasks: BackgroundTasks, db: Session = Depends(CRUD.get_db)):
    result = UserHandler.sign_up(
        db=db,
        payload=payload
    )
    background_tasks.add_task(func=UserHandler.send_verify_mail, email=result['email'], id_=result['id'])
    return result


@router.post('/refresh-token')
def refresh_token(payload: RefreshToken):
    ...


@router.post('/request-reset-password')
def request_reset_password(payload: RequestResetPassword):
    ...


@router.post('/reset-password')
def reset_password(payload: ResetPassword):
    ...


@router.get('/profile')
def get_profile():
    ...


@router.put('/profile')
def update_profile(profile: UpdateProfile):
    ...
