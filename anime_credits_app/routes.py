import os

from flask import render_template, request, redirect, url_for

from anime_credits_app import app, adc, db
import anime_credits_app.models as models
import anime_credits_app.mal_db as mal_db
import anime_credits_app.log_n_cache as lnc


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

    if category == 'people' and len(results) == 0:
        mal_id = adc.util.search_people_fallback(query)
        return redirect(url_for('person', mal_id = mal_id))

    return render_template('searching.html', results = results, category=category)


@app.route('/anime/<int:mal_id>')
def anime_staff(mal_id):

    if not lnc.check_page_visit('staff', mal_id):
        mal_db.acquire_staff(mal_id)

    anime = models.Anime.query.get(mal_id)

    lnc.register_page_visit('staff', mal_id)
    lnc.save_page_visits()

    return render_template("staff.html", anime = anime)


@app.route('/people/<int:mal_id>')
def person(mal_id):

    if not lnc.check_page_visit('people', mal_id):
        mal_db.acquire_person(mal_id)

    person = models.Person.query.get(mal_id)

    lnc.register_page_visit('people', mal_id)
    lnc.save_page_visits()

    return render_template('person.html', person = person)
