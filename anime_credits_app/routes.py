import os

from flask import render_template, request, redirect, url_for

from anime_credits_app import app, adc, db
import anime_credits_app.models as models
import anime_credits_app.mal_db as mal_db



from pathlib import Path
#print("routes", Path(__name__).resolve())

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        if 'query' in request.form:

            query = request.form['query']
            category = request.form['category']

            return redirect(url_for('search_options', category = category, query = query))
        else:
            return redirect(url_for('index'))



@app.route('/search/<category>/<query>')
def search_options(category, query):
    results = adc.mal.search_options(category, query, 10)
    return render_template('searching.html', results = results, category=category)


@app.route('/anime/<int:mal_id>')
def anime_staff(mal_id):
    # if adc.mal.check_file("anime", mal_id):
    #     anime_info = adc.mal.get_data_file("anime", mal_id)
    #     staff = adc.mal.get_data_file("staff", mal_id)

    #     print("staff was cached")
    # else:
    #     anime_info = adc.mal.get_anime_api(mal_id)
    #     staff = adc.mal.get_staff_api(mal_id)

    #     adc.mal.save_anime(anime_info)
    #     adc.mal.save_staff(mal_id, staff)

    #     print("staff downlaod from API")
    

    #temp
    mal_db.update_staff(mal_id)
    anime = models.Anime.query.get(mal_id)
    staff = anime.staff
    
    return render_template("staff-table.html",anime = anime,  staff = staff)


@app.route('/people/<int:mal_id>')
def person(mal_id):
    return f"Person {mal_id}"
