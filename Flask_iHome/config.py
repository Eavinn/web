# -*- coding:utf-8 -*-

import redis
import logging


class Config(object):
    """工程配置信息"""
    SECRET_KEY = "665FPU65q7pO9Z7fc/qRjWSD1lgGynkcqMwTfogvi9GAOsQGq84DlcHyYdkt88Zy"

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql://meng:ml6666@192.168.49.147:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "192.168.49.147"
    REDIS_PORT = 6379
    REDIS_DB = 2

    # flask_session的配置信息
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发模式下的配置"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产模式下的配置"""
    LOG_LEVEL = logging.WARN


MODE_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
