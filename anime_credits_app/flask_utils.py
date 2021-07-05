from flask import url_for
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import accumulate
import unicodedata
import locale

import json

import anime_credits_app
from anime_credits_app import app, log_n_cache, models

locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def image_path(resource, use_local_images:bool):
    # static/images/people/123.jpg

    if (not use_local_images) or (resource.local_image_url == None):
        return resource.image_url
    else:
        return url_for('static', filename=resource.local_image_url)
    
def truncate(string, length) -> str:
    return (string[:length] + '...') if len(string) > length else string

def average_studio_score(studio : models.Studio):
    score_sum = 0
    quantity = 0
    for anime in studio.anime:
        if anime.score is not None:
            score_sum += anime.score
            quantity += 1
    return round(score_sum / quantity ,2 )

def average_studio_favorites(studio : models.Studio):
    favorites_sum = 0
    quantity = 0
    for anime in studio.anime:
        if anime.favorites is not None:
            favorites_sum += anime.favorites
            quantity += 1
    return round(favorites_sum / quantity)

def average_studio_members(studio : models.Studio):
    members_sum = 0
    quantity = 0
    for anime in studio.anime:
        if anime.members is not None:
            members_sum += anime.members
            quantity += 1
    return round(members_sum / quantity)

@app.context_processor
def inject_python_functions():

    def staff_age(premiere : datetime, birthday : datetime):
        if birthday and premiere:
            return relativedelta(premiere, birthday).years
        else:
            return "-"
        

    return {
        'len' : len, 'staff_age' : staff_age, 'resource_name' : log_n_cache.get_resource_name, 'image_path' : image_path, 'truncate' : truncate,
        'average_studio_score' : average_studio_score, 'average_studio_favorites' : average_studio_favorites, 'average_studio_members' : average_studio_members
    }

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





            