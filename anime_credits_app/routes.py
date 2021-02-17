import time, sys

from flask import render_template, request, redirect, url_for, flash, session, abort
import celery.states
from celery.app.control import Inspect

from anime_credits_app import app, adc, tasks, models
import anime_credits_app.log_n_cache as lnc



from pathlib import Path
#print("routes", Path(__name__).resolve())

@app.route('/')
def index():
    app.logger.debug("Hemlo world from logger")
    app.logger.info("Hemlo world from logger")
    app.logger.warning("Hemlo world from logger")
    app.logger.error("Hemlo world from logger")
    app.logger.critical("Hemlo world from logger")
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return render_template('500.html'), 500


@app.route('/search', methods=['POST'])
def search():
    #print(request.form['search_form'])

    if 'query' in request.form:

        query = request.form['query']
        category = request.form['category']

        return redirect(url_for('search_options', category = category, query = query))
    else:
        return redirect(url_for('index'))

@app.route('/search/<category>/<query>')
def search_options(category, query):

    if category == 'studios':
        results = models.Studio.query.filter(models.Studio.name.contains(query)).all()
    else:
        results = adc.mal.search_options(category, query, 10)
        if category == 'people' and len(results) == 0:
            mal_id = adc.util.search_people_fallback(query)
            if mal_id:
                return redirect(url_for('content',category='people', mal_id = mal_id))

    return render_template('searching.html', results = results, category=category)

@app.route('/quick_search/<category>/<query>')
def quick_search(category, query):
    response = {}
    response['category'] = category

    if category == 'people':
        results = models.Person.query.filter(models.Person.name.contains(query)).all()
        results += models.Person.query.filter(models.Person.given_name.contains(query)).all()
        results += models.Person.query.filter(models.Person.family_name.contains(query)).all()
        response['results'] = [{'identifier':result.name, 'mal_id':result.mal_id} for result in results]

    elif category == 'studios':
        results = models.Studio.query.filter(models.Studio.name.contains(query)).all()
        response['results'] = [{'identifier':result.name, 'mal_id':result.mal_id} for result in results]

    elif category == 'anime':
        results = models.Anime.query.filter(models.Anime.title.contains(query)).all()
        results += models.Anime.query.filter(models.Anime.title_english.contains(query)).all()
        results += models.Anime.query.filter(models.Anime.title_japanese.contains(query)).all()
        response['results'] = [{'identifier':result.title, 'mal_id':result.mal_id} for result in results]

    else:
        response = []

    results = []
    for result in response['results']:
        if result not in results:
            results.append(result)

    response['results'] = results[:6]
    return response

    

@app.route('/downloading/<task_id>')
def page_downloading(task_id):
    task = tasks.update_resources_async.AsyncResult(task_id)

    if task.state == celery.states.FAILURE:
        response = {
            'state' : task.state,
            'info' : "Error while downloading"
        }
    else:
        response = {
            'state' : task.state,
            'info' : task.info
        }
    return response


@app.route('/<category>/<int:mal_id>')
def content(category, mal_id : int):

    if not adc.util.check_resource_exists(category, mal_id):
        abort(404)

    templates = {
        'anime' : "characters_staff.html",
        'people' : "person.html",
        'studios' : 'studio.html'
    }

    resource_models = {
        'anime' : models.Anime,
        'people' : models.Person,
        'studios' : models.Studio
    }

    page_status = lnc.check_page_update(category, mal_id, time_limit=app.config.get('DATA_EXPIRY_DAYS'))


    if page_status['being_created'] or page_status['scheduled_to_update']:
        return render_template('page_downloading.html', category=category, task_id = page_status['task_id'], downloading_right_now = page_status['being_created'])

    elif not page_status['exists']:
        task = tasks.update_resources_async.delay(category, mal_id, first_time=True)
        lnc.register_page_update_scheduled(category, mal_id, task.id)
        return render_template('page_downloading.html', category=category, task_id = task.id, downloading_right_now = False)

    elif page_status['needs_update']:
        resource = resource_models[category].query.get_or_404(mal_id)
        task = tasks.update_resources_async.delay(category, mal_id, first_time=False)

        return render_template(templates[category], resource = resource)
    else:
        resource = resource_models[category].query.get_or_404(mal_id)
        return render_template(templates[category], resource = resource)


@app.route('/tasksstatus')
def tasks_status():


    return render_template('tasks_status.html')



