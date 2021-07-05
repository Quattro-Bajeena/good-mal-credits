import os, yaml, logging, logging.config
import collections
from pathlib import Path
from datetime import time, timedelta
from yaml.loader import SafeLoader
from typing import Tuple


basedir = Path(__file__).resolve().parent


class Config(object):
    def __init__(self, _dict):
        self.__dict__.update(_dict)



def get_flask_config():
    with open('config.yaml', 'r') as f:
        config_dict = yaml.load(f, Loader=SafeLoader)
        # flask_config = collections.namedtuple("FlaskConfig", config_dict.keys())(*config_dict.values()) 
        flask_config = Config(config_dict)

    if not hasattr(flask_config, 'SQLALCHEMY_DATABASE_URI'):
        setattr(flask_config, 'SQLALCHEMY_DATABASE_URI','sqlite:///' + str(basedir / 'app.db') )
    flask_config.DATA_EXPIRY_DAYS = timedelta(days=flask_config.DATA_EXPIRY_DAYS)


    return flask_config

def get_celery_config():
    with open('celery_config.yaml', 'r') as f:
        config_dict = yaml.load(f, Loader=SafeLoader)
        # celery_config = collections.namedtuple("CeleryConfig", config_dict.keys())(*config_dict.values()) 
        celery_config = Config(config_dict)
    return celery_config


def config_loggers() -> logging.Logger:
    with open('logging_config.yaml', 'r') as f:
        config_dict = yaml.load(f, Loader=SafeLoader)
        logging.config.dictConfig(config_dict)
    return logging.getLogger('flask_logger')
    
    
    