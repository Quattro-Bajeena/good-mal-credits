from time import sleep
import logging
from celery.signals import after_setup_logger

from anime_credits_app import celery,logger,  mal_db, log_n_cache



@after_setup_logger.connect
def on_celery_setup_logging(**kwargs):
    logging.getLogger('flask_logger').handlers = logging.getLogger('celery_logger').handlers
    logging.getLogger('celery').handlers = logging.getLogger('celery_logger').handlers
    


@celery.task(bind=True)
def update_resources_async(self, resource_type, mal_id:int, first_time:bool):
    # it looks like when page is created in main flask app 
    # even after its commited to databse
    # the log and cache check page update tries to get it but its not there
    # so maybe waiting a little will help, but its a hack
    sleep(1)
    #task_id = str(self.request.id)
    try:
        page_status = log_n_cache.check_page_update(resource_type, mal_id)

        if first_time and page_status['exists']:
            return "Page was already created in the meantime"

        log_n_cache.register_page_update_start(resource_type, mal_id)

        # staff -> characters_staff
        resource_functions = {
            "anime" : mal_db.update_characters_staff,
            "people" : mal_db.update_person_credits,
            "studios" : mal_db.update_studio_page
        }
        resource_functions[resource_type](mal_id, use_cached=first_time, celery_task=self)
        log_n_cache.register_page_update_complete(resource_type,mal_id)
        
        return f'Page Updated - {resource_type}/{mal_id}'

    except Exception as e:
        log_n_cache.failed_page_update_cleanup(resource_type,mal_id)
        self.update_state(state='FAILURE', meta={'exc' : e})
        raise

