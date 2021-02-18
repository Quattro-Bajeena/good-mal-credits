from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from anime_credits_app.celery_config import make_celery
import anime_data_collector as adc
from app_config import config_loggers, get_flask_config, get_celery_config

app_root = Path(__file__).parent
adc.config.config_database(app_root)

logger = config_loggers()

app = Flask(__name__)
app.config.from_object(get_flask_config())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery = make_celery(app, get_celery_config())



from anime_credits_app import routes, models, flask_utils, mal_db, log_n_cache


print(app.config['SQLALCHEMY_DATABASE_URI'])






