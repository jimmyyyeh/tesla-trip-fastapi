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

router = APIRouter(tags=['user'])


@router.post('/verify')
def verify():
    ...


@router.post('/resend-verify')
def resend_verify():
    ...


@router.post('/sign-up')
def sign_up():
    ...


@router.post('/sign-in')
def sign_in():
    ...


@router.get('/profile')
def get_profile():
    ...


@router.put('/profile')
def update_profile():
    ...


@router.post('/refresh-token')
def refresh_token():
    ...


@router.post('/request-reset-password')
def request_reset_password():
    ...


@router.post('/reset-password')
def reset_password():
    ...
