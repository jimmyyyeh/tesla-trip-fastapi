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

from random import choice

import pytest

from utils.const import Const


@pytest.fixture(scope='class')
def user_info():
    user_info = {
        'username': 'jimmy',
        'password': '1234567890',
        'nickname': 'jimmy not nick',
        'email': 'chienfeng0719@hotmail.com',
        'birthday': '1996-07-19',
        'sex': choice(list(Const.Sex.get_elements())),
    }
    return user_info
