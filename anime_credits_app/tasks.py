from anime_credits_app import celery, mal_db, log_n_cache


@celery.task(bind=True)
def update_resources_async(self, resource_type, mal_id:int, first_time:bool):

    #task_id = str(self.request.id)

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
    try:
        resource_functions[resource_type](mal_id, use_cached=first_time, celery_task=self)
    except Exception as e:
        log_n_cache.failed_page_update_cleanup(resource_type,mal_id)
        self.update_state(state='FAILURE', meta={'exc' : e})
        raise
    
    log_n_cache.register_page_update_complete(resource_type,mal_id)
    return 'Page Updated'

