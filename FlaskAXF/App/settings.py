import os

from flask_uploads import IMAGES
from redis import Redis


def get_db_url(db_info):
    engine = db_info.get("ENGINE") or "sqlite"
    driver = db_info.get("DRIVER") or "sqlite"
    user = db_info.get("USER") or ""
    password = db_info.get("PASSWORD") or ""
    host = db_info.get("HOST") or ""
    port = db_info.get("PORT") or ""
    name = db_info.get("NAME") or ""

    return '{}+{}://{}:{}@{}:{}/{}'.format(engine, driver, user, password, host, port, name)


class Config:

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'ROCK'

    # SESSION_COOKIE_SECURE = True
    #
    # SESSION_USE_SIGNER = True

    # session redis
    SESSION_TYPE = "redis"

    # cache redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '47.93.254.125'
    CACHE_REDIS_PORT = 6379

    # 文件上传
    UPLOADS_DEFAULT_DEST = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/icons'
    UPLOADED_FILES_ALLOW = IMAGES


class DevelopConfig(Config):
    DEBUG = True

    db_info = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'FlaskAXF'
    }
    SESSION_REDIS = Redis(host='47.93.254.125', port='6379')

    SQLALCHEMY_DATABASE_URI = get_db_url(db_info)


class TestingConfig(Config):
    DEBUG = True

    db_info = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'FlaskAXF'
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(db_info)


class StagingConfig(Config):
    DEBUG = True

    db_info = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'FlaskAXF'
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(db_info)


class ProductConfig(Config):
    DEBUG = True

    db_info = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'FlaskAXF'
    }

    SQLALCHEMY_DATABASE_URI = get_db_url(db_info)


envs = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig,

}