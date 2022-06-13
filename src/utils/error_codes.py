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


class ErrorCodes:
    INTERNAL_SERVER_ERROR = 500

    USER_NOT_EXISTS = 1001  # 使用者不存在
    USER_INVALIDATE = 1002  # 使用者授權無效(密碼錯誤)
    USER_ALREADY_EXISTS = 1003  # 使用者已存在
    USER_UNVERIFIED = 1004  # 使用者未驗證
    TOKEN_INVALIDATE = 1005  # 無效授權
    TOKEN_EXPIRED = 1006  # 授權逾時
    TOKEN_MISSING = 1007  # headers 未帶授權
    VERIFY_TOKEN_NOT_EXISTS = 1008  # 驗證token不存在
    RESET_PASSWORD_TOKEN_NOT_EXISTS = 1009  # 重設密碼token不存在
    RESET_PASSWORD_TOKEN_INVALIDATE = 1010  # 重設密碼token錯誤
    ROLE_INVALIDATE = 1011  # 身份不符

    PARAMETER_ERROR = 2001  # 參數錯誤
    DATA_NOT_FOUND = 2022  # 資料不存在

    INSUFFICIENT_POINT = 3001  # 點數不足
    INSUFFICIENT_PRODUCT_STOCK = 3002  # 庫存不足
