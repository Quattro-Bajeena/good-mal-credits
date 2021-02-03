from time import sleep

from anime_credits_app import celery, adc, mal_db, models, log_n_cache




@celery.task(bind=True)
def add_1_async(self, param1):
    self.update_state(state='PENDING')
    for i in range(param1):
        self.update_state(state='PENDING', meta={'current': i, 'total' : param1 })
        sleep(1)
    self.update_state(state='COMPLETE')
    return param1 + 1


@celery.task
def database_test():
    mal_db.acquire_staff(39990)
    anime = models.Anime.query.get(39990)
    return anime.title

@celery.task(bind=True)
def update_resources_async(self, resource_type, mal_id, use_cached):
    resource_functions = {
        "staff" : mal_db.update_staff,
        "people" : mal_db.update_person_credits
    }

    resource_functions[resource_type](mal_id, use_cached, self)

@celery.task
def save_page_visits_async():
    log_n_cache.save_page_updates()
