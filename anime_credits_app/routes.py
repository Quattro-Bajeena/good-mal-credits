from anime_credits_app import app, adc
from flask import render_template, request, redirect, url_for

# from anime_credits_app import mal_api
# from anime_credits_app import anime_db_config as ani_conf
import os

from pathlib import Path
#print("routes", Path(__name__).resolve())

@app.route('/')
def index():
    print(adc.config.anime_folder.is_dir())
    print(adc.config.anime_folder)
    return render_template('base.html')

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':

        query = request.form['query']
        if not query:
            return redirect(url_for('index'))

        category = request.form['search-category']
        print(query, category)
        
        mal_id = adc.mal.id_from_search(category, query)
        print(mal_id)

        if category == "anime":
            return redirect(url_for('anime_staff', mal_id = mal_id))
        else:
            return redirect(url_for('index'))


@app.route('/search-options', methods=('GET', 'POST'))
def search_with_options():
    if request.method == 'POST':
        query = request.form['query']
        if not query:
            return redirect(url_for('index'))
        category = request.form['search-category']

        return redirect(url_for('search_options', category = category, query = query))



@app.route('/search/<category>/<query>')
def search_options(category, query):
    results = adc.mal.search_options(category, query, 10)
    return render_template('searching.html', results = results, category=category)


@app.route('/anime/<int:mal_id>')
def anime_staff(mal_id):
    if adc.mal.check_file("anime", mal_id):
        anime_info = adc.mal.get_data_file("anime", mal_id)
        staff = adc.mal.get_data_file("staff", mal_id)

        print("staff was cached")
    else:
        anime_info = adc.mal.get_anime_api(mal_id)
        staff = adc.mal.get_staff_api(mal_id)

        adc.mal.save_anime(anime_info)
        adc.mal.save_staff(mal_id, staff)

        print("staff downlaod from API")
    

    return render_template("staff-table.html",anime = anime_info,  staff = staff["staff"])


@app.route('/people/<int:mal_id>')
def person(mal_id):
    return f"Person {mal_id}"
