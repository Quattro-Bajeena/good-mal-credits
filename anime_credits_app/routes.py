import os
from datetime import timedelta

from flask import render_template, request, redirect, url_for, flash, session

from anime_credits_app import app, adc, db, tasks, models, mal_db, celery
import anime_credits_app.log_n_cache as lnc



from pathlib import Path
#print("routes", Path(__name__).resolve())

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/test_celery', methods=['POST'] )
def test_celery():
    if request.method == 'POST':
        task = tasks.add_1_async.delay(10)
        return redirect(url_for('download', task_id = task.id))

@app.route('/celery_result/<task_id>')
def celery_results(task_id):
    task = tasks.add_1_async.AsyncResult(task_id)

    response = {
        'state' : task.state,
        'info' : task.info
    }


    return response

@app.route('/search', methods=['POST'])
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

@app.route('/downloading/<task_id>')
def page_downloading(task_id):
    task = tasks.update_resources_async.AsyncResult(task_id)

    response = {
        'state' : task.state,
        'result': task.result,
        'info' : task.info
    }
    # print(response)
    return response


@app.route('/download/<task_id>')
def download(task_id):
    return render_template('page_downloading.html', category='staff', task_id = task_id) 

@app.route('/anime/<int:mal_id>')
def anime_staff(mal_id):
    
    category = 'staff'
    page_status = lnc.check_page_update(category, mal_id, time_limit=app.config.get('DATA_EXPIRY_DAYS'))

    print(page_status)

    if page_status['being_created']:
        print("1111111111111")
        return render_template('page_downloading.html', category=category, task_id = page_status['task_id'])

    elif not page_status['exists']:
        print("2222222222222222")
        
        task = tasks.update_resources_async.delay(category, mal_id, use_cached=True)


        return render_template('page_downloading.html', category=category, task_id = task.id)

    elif page_status['needs_update']:
        print("33333333333333")
        anime = models.Anime.query.get(mal_id)
        task = tasks.update_resources_async.delay(category, mal_id, use_cached=False)

        return render_template("staff.html", anime = anime)

    else:
        print("4444444444444")
        anime = models.Anime.query.get(mal_id)
        return render_template("staff.html", anime = anime)




@app.route('/people/<int:mal_id>')
def person(mal_id):

    category = 'people'
    page_status = lnc.check_page_update(category, mal_id, time_limit=app.config.get('DATA_EXPIRY_DAYS'))
    print(page_status)

    if page_status['being_created']:
        print("1111111111111")
        return render_template('page_downloading.html', category=category, task_id = page_status['task_id'])

    elif not page_status['exists']:
        print("2222222222222222")
        task = tasks.update_resources_async.delay(category, mal_id, use_cached=True)

        return render_template('page_downloading.html', category=category, task_id = task.id)

    elif page_status['needs_update']:
        print("33333333333333")
        person = models.Person.query.get(mal_id)
        task = tasks.update_resources_async.delay(category, mal_id, use_cached=False)

        return render_template("person.html", person = person)
    else:
        print("4444444444444")
        person = models.Person.query.get(mal_id)
        return render_template("person.html", person = person)
