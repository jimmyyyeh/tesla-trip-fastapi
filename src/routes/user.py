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
from database.db_handler import DBHandler
from utils import response_models
from utils.auth_tools import AuthValidator
from utils.payload_schemas import Verify, ResendVerify, SignIn, SignUp, UpdateProfile, ResetPassword, \
    RequestResetPassword
from utils.response_models import Response, ResponseHandler

router = APIRouter(tags=['user'])
general_auth = AuthValidator()


@router.post('/verify', response_model=response_models.SuccessOrNot)
async def verify(payload: Verify, db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.verify(
        db=db,
        verify_token=payload.token
    )
    return ResponseHandler.response(result=result)


@router.post('/resend-verify', response_model=response_models.SuccessOrNot)
async def resend_verify(payload: ResendVerify, background_tasks: BackgroundTasks,
                        db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.resend_verify(
        db=db,
        username=payload.username
    )
    background_tasks.add_task(func=UserHandler.send_verify_mail, id_=result['id'], email=result['email'])
    return ResponseHandler.response(result=bool(result))


@router.post('/sign-in', response_model=Response[response_models.SignIn])
async def sign_in(payload: SignIn, db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.sign_in(
        db=db,
        payload=payload
    )
    return ResponseHandler.response(result=result)


@router.post('/sign-up', response_model=Response[response_models.SignUp])
async def sign_up(payload: SignUp, background_tasks: BackgroundTasks, db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.sign_up(
        db=db,
        payload=payload
    )
    background_tasks.add_task(func=UserHandler.send_verify_mail, id_=result['id'], email=result['email'])
    return ResponseHandler.response(result=result)


@router.post('/request-reset-password', response_model=response_models.SuccessOrNot)
async def request_reset_password(payload: RequestResetPassword,
                                 background_tasks: BackgroundTasks,
                                 db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.request_reset_password(
        db=db,
        email=payload.email
    )
    background_tasks.add_task(func=UserHandler.send_reset_password_mail, id_=result['id'], email=result['email'])
    return ResponseHandler.response(result=bool(result))


@router.post('/reset-password', response_model=response_models.SuccessOrNot)
async def reset_password(payload: ResetPassword, db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.reset_password(
        db=db,
        reset_token=payload.token,
        username=payload.username,
        password=payload.password
    )
    return ResponseHandler.response(result=result)


@router.get('/profile', response_model=Response[response_models.UserBase])
def get_profile(user: dict = Depends(general_auth)):
    return user


@router.put('/profile', response_model=Response[response_models.SignIn])
async def update_profile(profile: UpdateProfile,
                         user: dict = Depends(general_auth),
                         db: Session = Depends(DBHandler.get_db)):
    result = await UserHandler.update_profile(
        db=db,
        user=user,
        email=profile.email,
        nickname=profile.nickname
    )
    return ResponseHandler.response(result=result)
