import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

basedir = Path(__file__).resolve().parent



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'app.db')

    #print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    DATA_EXPIRY_DAYS = timedelta(days=int(os.environ.get('DATA_EXPIRY_DAYS'))) 
    