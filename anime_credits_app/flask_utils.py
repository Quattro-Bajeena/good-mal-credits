from flask import url_for
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import unicodedata
import locale

import json

import anime_credits_app
from anime_credits_app import app, log_n_cache

locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def image_path(resource):
    # static/images/people/123.jpg
    if resource.local_image_url == None:
        return resource.image_url
    else:
        return url_for('static', filename=resource.local_image_url)
    

@app.context_processor
def inject_python_functions():

    def staff_age(premiere : datetime, birthday : datetime):
        if birthday and premiere:
            return relativedelta(premiere, birthday).years
        else:
            return "-"
        

    return {'len' : len, 'staff_age' : staff_age, 'resource_name' : log_n_cache.get_resource_name, 'image_path' : image_path}

@app.template_filter('format_percentage')
def format_percentage(percentage:float):
    return "{:.1f}%".format(percentage)

@app.template_filter('format_year')
def format_datetime(value):
    if value:
        return value.strftime('%Y')
        #return value.strftime('%Y-%m-%d')
    else:
        return "-"

@app.template_filter('format_date')
def format_datetime(value):
    if value:
        return value.strftime('%Y-%m-%d')
    else:
        return "-"

@app.template_filter('format_big_number')
def format_big_number(value):
    # javscript sort function assumes that values will be space separated, and they are because setLocale is pl_PL,
    # so value:n <- that n makes it according to this locale
    
    if value:
        return f"{value:n}"
    else:
        return "-"





            