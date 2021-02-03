import os

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
        return redirect(url_for('celery_results', task_id = task.id))

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

@app.route('/downloading/<category>/<int:mal_id>/<task_id>')
def page_downloading(category, mal_id, task_id):
    task = tasks.update_resources_async.AsyncResult(task_id)

    response = {
        'state' : task.state,
        'result': task.result,
        'info' : task.info
    }

    if task.state != 'SUCCESS':
        return response
    else:
        return redirect(url_for('anime_staff', mal_id=mal_id))


@app.route('/anime/<int:mal_id>')
def anime_staff(mal_id):

    page_status = lnc.check_page_update('staff', mal_id)

    if page_status['creating']:
        print("1111111111111")
        return render_template('page_downloading.html', category='staff',
         task_id = page_status['task_id'])

    elif not page_status['exists']:
        print("2222222222222222")
        task = tasks.update_resources_async.apply_async(args=['staff', mal_id, True], countdown=5)
        lnc.create_page_entry('staff', mal_id, task.id)
        return redirect(url_for('page_downloading',category='staff', mal_id = mal_id, task_id = task.id))
        #return render_template('page_downloading.html', category='staff', task_id = task.id)

    elif page_status['needs_update'] and not page_status['updating']:
        print("33333333333333")
        anime = models.Anime.query.get(mal_id)
        
        task = tasks.update_resources_async.apply_async(args=['staff', mal_id, False], countdown=10)
        lnc.register_page_start_update("staff", mal_id, task.id)
        return render_template("staff.html", anime = anime)

    else:
        print("4444444444444")
        anime = models.Anime.query.get(mal_id)
        return render_template("staff.html", anime = anime)


@app.route('/people/<int:mal_id>')
def person(mal_id):

    if not lnc.check_page_update('people', mal_id)['exists']:
        tasks.acquire_resources_async.delay('people', mal_id)
        return "Anime not yet in databse, come back in 5 minutes"

    else:
        person = models.Person.query.get(mal_id)

    return render_template('person.html', person = person)
