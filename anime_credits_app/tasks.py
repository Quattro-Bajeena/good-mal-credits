from time import sleep

from anime_credits_app import celery, adc, mal_db, models, log_n_cache





@celery.task(bind=True)
def add_1_async(self, param1):
    self.update_state(state='PENDING', meta={'current': 0, 'total' : param1, 'status': 'starting'})
    sleep(1)
    for i in range(param1):
        self.update_state(state='PENDING', meta={'current': i, 'total' : param1, 'status' : 'looping' })
        sleep(1)
    
    self.update_state(state='COMPLETED', meta={'current': param1, 'total' : param1, 'status' : 'finishing' })
    sleep(1)
    return param1 + 1


@celery.task
def database_test():
    mal_db.acquire_staff(39990)
    anime = models.Anime.query.get(39990)
    return anime.title

@celery.task(bind=True)
def update_resources_async(self, resource_type, mal_id, use_cached, first_time):

    task_id = str(self.request.id)

    log_n_cache.register_page_update_start(resource_type, mal_id,task_id)

    resource_functions = {
        "staff" : mal_db.update_staff,
        "people" : mal_db.update_person_credits
    }
    try:
        resource_functions[resource_type](mal_id, use_cached, self)
    except Exception as e:
        log_n_cache.failed_page_update_cleanup(mal_id)
        raise
        #return "Update Failed"
    
    log_n_cache.register_page_update_complete(mal_id)
    return 'Page Updated'

@celery.task
def save_page_visits_async():
    log_n_cache.save_page_updates()
