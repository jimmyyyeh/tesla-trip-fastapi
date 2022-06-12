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

import json

from database.redis_manager import redis_instance


class RedisKey:
    @staticmethod
    def verify_user(verify_token):
        return f'verify_user:{verify_token}'

    @staticmethod
    def reset_password(reset_token):
        return f'reset_password:{reset_token}'

    @staticmethod
    def redeem_product(token):
        return f'redeem_product:{token}'


class RedisHandler:
    @staticmethod
    def set_verify_user(verify_token, id_):
        key = RedisKey.verify_user(
            verify_token=verify_token
        )
        redis_instance.set(key, value=id_, ex=60 * 5)

    @staticmethod
    def get_verify_user(verify_token):
        key = RedisKey.verify_user(
            verify_token=verify_token
        )
        value = redis_instance.get(key)
        return value

    @staticmethod
    def delete_verify_user(verify_token):
        key = RedisKey.verify_user(
            verify_token=verify_token
        )
        redis_instance.delete(key)

    @staticmethod
    def set_reset_password(reset_token, id_):
        key = RedisKey.reset_password(
            reset_token=reset_token
        )
        redis_instance.set(key, value=id_, ex=60 * 5)

    @staticmethod
    def get_reset_password(reset_token):
        key = RedisKey.reset_password(
            reset_token=reset_token
        )
        value = redis_instance.get(key)
        return value

    @staticmethod
    def delete_reset_password(reset_token):
        key = RedisKey.reset_password(
            reset_token=reset_token
        )
        redis_instance.delete(key)

    @staticmethod
    def set_redeem_product(token, content):
        key = RedisKey.redeem_product(token=token)
        value = json.dumps(content)
        redis_instance.set(key, value, ex=60 * 5)

    @staticmethod
    def get_redeem_product(token):
        key = RedisKey.redeem_product(token=token)
        value = redis_instance.get(key)
        return json.loads(value) if value else None

    @staticmethod
    def delete_redeem_product(token):
        key = RedisKey.redeem_product(token=token)
        redis_instance.delete(key)
