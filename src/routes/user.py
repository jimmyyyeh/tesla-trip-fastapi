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
from utils.payload_schema import Verify, ResendVerify, SignIn, SignUp, UpdateProfile, RefreshToken, ResetPassword, \
    RequestResetPassword

router = APIRouter(tags=['user'])


@router.post('/verify')
def verify(payload: Verify):
    ...


@router.post('/resend-verify')
def resend_verify(payload: ResendVerify):
    ...


@router.post('/sign-in')
def sign_in(payload: SignIn):
    ...


@router.post('/sign-up')
def sign_up(payload: SignUp):
    ...


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
