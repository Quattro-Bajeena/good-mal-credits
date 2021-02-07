from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
import json

from anime_credits_app import app_root, db
from anime_credits_app.models import PageStatus




def register_page_update_start(category, mal_id, task_id):
    log = PageStatus.query.get(mal_id)
    if not log:
        log = PageStatus(
            mal_id = mal_id,
            category=category,
            exists = False,
            updating=True,
            task_id = task_id
        )
        db.session.add(log)
        print("created new page log")
    else:
        log.updating = True
        log.task_id = task_id


    print("register_page_update_start")
    db.session.commit()


def register_page_update_complete(mal_id):
    log = PageStatus.query.get(mal_id)
    log.updating = False
    log.exists = True
    log.task_id = ''
    log.last_modified = datetime.now()
    db.session.commit()
    print("register_page_update_complete")

def failed_page_update_cleanup(mal_id):
    db.session.rollback()

    log = PageStatus.query.get(mal_id)
    log.updating = False
    log.task_id = ''
    db.session.commit()
    print("failed_page_update_cleanup")
    

def check_page_update(category, mal_id, time_limit : timedelta = None):

    # possible page states

    # -not yet in database                                      -> exists:False, updating:False, task_id : None (crash)
    # -in database but not created and updating at the moment   -> exists:False, updating:True, task_id : xxx
    # -in databse but not created and not updating              -> exists:False, updating:False, task_id : None
    # -in database and created                                  -> exists: True, updating:False, task_id  : NOne

    log = PageStatus.query.get(mal_id)
    print("log", log)
    in_db = bool(log)
    exists = in_db and log.exists

    updating = in_db and log.updating
    task_id =  updating and log.task_id

    needs_update = exists and (not updating) and (time_limit and ( (datetime.now() - log.last_modified) > time_limit) )

    being_created = not exists and updating

    return {
        'exists' : exists, 
        'being_created' : being_created,
        'needs_update': needs_update,
        'updating' : updating,
        'task_id' : task_id
        }




