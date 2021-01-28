from anime_credits_app import app
from flask import render_template

@app.route('/')
def index():
    user = {'username': 'General Kenobi'}
    return render_template('index.html', title='Home', user = user)