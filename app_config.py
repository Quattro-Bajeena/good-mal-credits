import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

basedir = Path(__file__).resolve().parent



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + str(basedir / 'app.db')

    #print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_EXPIRY_DAYS = timedelta(days=int(os.environ.get('DATA_EXPIRY_DAYS'))) 

class CeleryConfig(object):
    broker_url = os.environ.get('CELERY_BROKER_URL')
    result_backend = os.environ.get('CELERY_RESULT_BACKEND')

    worker_prefetch_multiplier = os.environ.get('CELERY_WORKER_PREFETCH_MULTIPLIER', 1)
    worker_concurrency = os.environ.get('CELERY_WORKER_CONCURRENCY', 1)
    worker_redirect_stdouts_level = os.environ.get('CELERY_LOG_LEVEL', 'INFO')


    