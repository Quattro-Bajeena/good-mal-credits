from datetime import date, datetime, timedelta

from anime_credits_app import db, logger
from anime_credits_app import models
from anime_credits_app.models import PageStatus



def page_id_maker(category, mal_id)->str:
    return f"{category}-{mal_id}"


#Page status life cycle
#                                       update completed
# creation/register -> update start ->
#                                       update cleanup
def register_page_update_scheduled(category, mal_id, task_id):
    page_id = page_id_maker(category, mal_id)
    log = PageStatus.query.get(page_id)
    if not log:
        log = PageStatus(
            id = page_id,
            mal_id = mal_id,
            category=category,
            exists = False,

            updating=False,
            scheduled_to_update = True,
            scheduled_time = datetime.now(),
            task_id = task_id,
            update_failed = False
        )
        db.session.add(log)
        logger.info(f"scheduled to update, created new page log - {page_id}")
    else:
        log.scheduled_to_update = True
        log.scheduled_time = datetime.now()
        log.updating = False
        log.task_id = task_id
        

    db.session.commit()
    logger.info(f"Registered page update scheduled - {page_id}")
    



def register_page_update_start(category, mal_id):
    page_id = page_id_maker(category, mal_id)
    log = PageStatus.query.get(page_id)
    log.updating = True
    log.scheduled_to_update = False
    log.scheduled_time = None
    log.update_failed = False
    db.session.commit()
    logger.info("Page update started")


def register_page_update_complete(category, mal_id):
    page_id = page_id_maker(category, mal_id)
    log = PageStatus.query.get(page_id)
    log.updating = False
    log.exists = True
    log.task_id = None
    log.last_modified = datetime.now()
    db.session.commit()
    logger.info(f"Page update completed - {page_id}")

def failed_page_update_cleanup(category, mal_id):
    page_id = page_id_maker(category, mal_id)
    db.session.rollback()

    log = PageStatus.query.get(page_id)
    log.updating = False
    log.scheduled_to_update = False
    log.scheduled_time = None
    log.task_id = None
    log.update_failed = True
    db.session.commit()
    logger.error(f"Failed Page Update - {page_id}. Cleaned up")
    

def check_page_update(category, mal_id, time_limit : timedelta = None):

    # possible page states

    # -not yet in database                                      -> exists:False, updating:False, task_id : None (crash)
    # -in database but not created and updating at the moment   -> exists:False, updating:True, task_id : xxx
    # -in databse but not created and not updating              -> exists:False, updating:False, task_id : None
    # -in database and created                                  -> exists: True, updating:False, task_id  : None
    # -in databse and created and scheduled to update           -> exists: Truye,udpating: False, task_id : xxxx
    page_id = page_id_maker(category, mal_id)
    log = PageStatus.query.get(page_id)
    # logger.info(f"check_page_update - log: {log} ")
    in_db = bool(log)
    exists = in_db and log.exists

    updating = in_db and log.updating
    scheduled_to_update = in_db and log.scheduled_to_update
    scheduled_time = scheduled_to_update and log.scheduled_time
    task_id =  (updating or scheduled_to_update) and log.task_id
    update_failed = log.update_failed

    needs_update = exists and (not updating) and (time_limit and ( (datetime.now() - log.last_modified) > time_limit) )

    being_created = not exists and updating

    return {
        'exists' : exists, 
        'being_created' : being_created,
        'needs_update': needs_update,
        'updating' : updating,
        'scheduled_to_update' : scheduled_to_update,
        'task_id' : task_id,
        'scheduled_time' : scheduled_time,
        'update_failed' : update_failed
        }


def get_resource_name(resource_type, resource_id):
    resource_models = {
        'anime' : models.Anime,
        'people' : models.Person,
        'studios' : models.Studio
    }
    
    #print(resource_type, resource_id)
    resource = resource_models[resource_type].query.get(resource_id)
    #print(resource)
    if resource:
        if hasattr(resource, 'name'):
            return resource.name

        elif hasattr(resource, 'title'):
            return resource.title

        else:
            return resource.mal_id
    else:
        return "not known"
    

