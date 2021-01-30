from flask import Flask
import anime_data_collector as adc

app = Flask(__name__)

from anime_credits_app import config
from anime_credits_app import routes

