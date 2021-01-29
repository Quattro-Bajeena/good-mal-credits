from anime_credits_app import app
from flask import render_template, request, redirect, url_for

from anime_credits_app import mal_api
from anime_credits_app import anime_db_config as ani_conf
import os

from pathlib import Path

@app.route('/')
def index():
    print(ani_conf.anime_folder.is_dir())
    print(ani_conf.anime_folder)
    return render_template('index.html')

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':

        query = request.form['query']
        if not query:
            return redirect(url_for('index'))

        category = request.form['search-category']
        print(query, category)
        
        mal_id = mal_api.id_from_search(category, query)
        print(mal_id)


        if category == "anime":
            return redirect(url_for('anime_staff', mal_id = mal_id))
        else:
            return redirect(url_for('index'))

@app.route('/anime/<int:mal_id>')
def anime_staff(mal_id):
    staff = [
            {"name" : "Hideaki Anno", "position" : "Our God"},
            {"name" : "Hayao Miyazaki", "position" : "Our Savior"},
            {"name" : "Yoshiyuki Tomino", "position" : "Our Master"}
        ]

    if mal_api.check_file("staff", mal_id):
        mal_staff = mal_api.get_data_file("staff", mal_id)
        print("staff was cached")
    else:
        mal_staff = mal_api.get_staff_api(mal_id)
        mal_api.save_staff(mal_id, mal_staff)
        print("staff downlaod from API")
    
    staff = []
    for person in mal_staff["staff"]:
        for position in person["positions"]:
            staff.append({"name" : person["name"], "position": position})

    return render_template("staff-table.html", staff = staff)
