from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from anime_credits_app.celery_config import make_celery
import anime_data_collector as adc
from app_config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery = make_celery(app)


app_root = Path(__file__).parent
adc.config.config_database(app_root)

from anime_credits_app import routes, models, config, mal_db, log_n_cache






