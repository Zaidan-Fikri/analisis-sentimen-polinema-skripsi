import os

from flask import app

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))

    SECRET_KEY = 'abcsj'
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    JWT_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_NOTIFICATION = False
    SQLALCHEMY_RECORD_QUERIES = True
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT=False