from pathlib import Path
import logging.config, yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from yaml.loader import SafeLoader


from anime_credits_app.celery_config import make_celery
import anime_data_collector as adc
from app_config import Config, CeleryConfig

app_root = Path(__file__).parent
adc.config.config_database(app_root)

with open('logging_config.yaml') as f:
    config_dict = yaml.load(f, Loader=SafeLoader)
    logging.config.dictConfig(config_dict)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery = make_celery(app, CeleryConfig)


from anime_credits_app import routes, models, flask_utils, mal_db, log_n_cache







