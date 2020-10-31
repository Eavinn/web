import redis
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import MODE_MAP
from ihome.utils.commons import RegexConverter


db = SQLAlchemy()
redis_store = None


def register_blueprint(app):
    from ihome.api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")
    from ihome.web_html import html
    app.register_blueprint(html)


def set_logging(log_level):
    logger = logging.getLogger()
    logger.setLevel(level=log_level)
    file_log_handler = RotatingFileHandler("logs/log.txt", maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    file_log_handler.setFormatter(formatter)
    logger.addHandler(file_log_handler)


def create_app(config_name):
    """通过传入不同的配置名字，初始化其对应配置的应用实例"""
    app = Flask(__name__)
    # 配置
    config_obj = MODE_MAP[config_name]
    app.config.from_object(config_obj)

    # 配置日志信息
    set_logging(config_obj.LOG_LEVEL)

    # 添加路由转换器
    app.url_map.converters["re"] = RegexConverter
    # 数据库
    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_obj.REDIS_HOST, port=config_obj.REDIS_PORT, db=config_obj.REDIS_DB,
                                    decode_responses=True)

    # 开启 csrf 保护
    CSRFProtect(app)
    # 开启Session
    Session(app)
    # 注册蓝图
    register_blueprint(app)

    return app
