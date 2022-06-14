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

import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    environment: str = 'develop'
    api_domain: str
    web_domain: str
    static_path: str = '/app/static/'

    # mysql
    db_name: str
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int = 3306

    # redis
    redis_host: str
    redis_password: str = None
    redis_port: int = 6379

    sqlalchemy_track_modifications: bool = False
    json_as_ascii: bool = False

    # JWT
    access_token_expire_time: int = 60 * 5
    refresh_token_expire_time: int = 60 * 60 * 24  # 一天
    salt: str

    # mail
    mail_server: str = 'smtp.gmail.com'
    mail_port: int = 465
    mail_use_ssl: bool = True
    mail_max_emails: int = 10
    mail_username: str
    mail_password: str

    class Config:
        env_file = '.env'
