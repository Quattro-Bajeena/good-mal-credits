from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

import anime_credits_app
from anime_credits_app import app




@app.context_processor
def inject_python_functions():

    def staff_age(premiere : datetime, birthday : datetime):
        if birthday and premiere:
            return relativedelta(premiere, birthday).years
        else:
            return "-"
        

    return {'len' : len, 'staff_age' : staff_age}

@app.template_filter('format_date')
def format_datetime(value):
    if value:
        return value.strftime('%Y-%m-%d')
    else:
        return "-"





            