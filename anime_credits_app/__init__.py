from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import anime_data_collector as adc
from app_config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from anime_credits_app import routes, models, config, mal_db


