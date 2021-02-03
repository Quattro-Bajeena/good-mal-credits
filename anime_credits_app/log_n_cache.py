from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
import json

from anime_credits_app import app_root, db
from anime_credits_app.models import PageStatus


def create_page_entry(category, mal_id, task_id):
    new_log = PageStatus(
            mal_id = mal_id,
            category=category,
            creating=True,
            updating=False,
            task_id = task_id
        )
    db.session.add(new_log)
    db.session.commit()

def register_page_start_update(category, mal_id, task_id):
    log = PageStatus.query.get(mal_id)
    log.task_id = task_id
    log.updating = True
    db.session.commit()
    

def register_page_update(category, mal_id):
    log = PageStatus.query.get(mal_id)
    if not log:
        new_log = PageStatus(
            mal_id = mal_id,
            category=category,
            last_modified = datetime.now(),
            creating=False,
            updating=False
            
        )
        db.session.add(new_log)
    else:
        log.creating = False
        log.updating = False
        log.last_modified = datetime.now()

    #no db.sesson.commit cos it will be called inside the big update functions, that will do it right after
    


def check_page_update(category, mal_id, time_limit : timedelta = None):

    log = PageStatus.query.get(mal_id)

    exists = False
    needs_update = False
    creating = False
    updating = False
    

    exists = bool(log)
    needs_update = exists and time_limit and (datetime.now() - log.last_modified) > time_limit 
    creating = exists and log.creating
    updating = exists and log.updating
    task_id = exists and (creating or updating) and log.task_id

    return {
        'exists' : exists, 'needs_update': needs_update,
        'creating' : creating, 'updating' : updating,
        'task_id' : task_id
        }




