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


class ConstTemplate:
    _INVALID_TYPE = {classmethod, staticmethod}

    @classmethod
    def get_elements(cls):
        elements = set()
        for k, v in cls.__dict__.items():
            if k.startswith('_') or type(v) in cls._INVALID_TYPE:
                continue
            elements.add(v)
        return elements
