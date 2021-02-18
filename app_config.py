import os, yaml, logging, logging.config
import collections
from pathlib import Path
from dotenv import load_dotenv
from datetime import time, timedelta
from yaml.loader import SafeLoader
from typing import Tuple

# load_dotenv()

basedir = Path(__file__).resolve().parent


# class Config(object):
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
#         'sqlite:///' + str(basedir / 'app.db')

#     #print(SQLALCHEMY_DATABASE_URI)
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     DATA_EXPIRY_DAYS = timedelta(days=int(os.environ.get('DATA_EXPIRY_DAYS'))) 

# class CeleryConfig(object):
#     broker_url = os.environ.get('CELERY_BROKER_URL')
#     result_backend = os.environ.get('CELERY_RESULT_BACKEND')

#     worker_prefetch_multiplier = int(os.environ.get('CELERY_WORKER_PREFETCH_MULTIPLIER', 1))

#     worker_concurrency = int(os.environ.get('CELERY_WORKER_CONCURRENCY', 1))

#     worker_hijack_root_logger = bool(int(os.environ.get('CELERY_WORKER_HIJACK_ROOT_LOGGER', 1)))

#     worker_redirect_stdouts = bool(int(os.environ.get('CELERY_WORKER_REDIRECT_STDOUTS', 1)))
#     worker_redirect_stdouts_level = os.environ.get('CELERY_REDIRECT_STDOUT_LEVEL', 'INFO')

#     worker_log_format = os.environ.get('CELERY_WORKER_LOG_FORMAT')
#     worker_task_log_format = os.environ.get('CELERY_WORKER_TASK_LOG_FORMAT')


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
    
    
    