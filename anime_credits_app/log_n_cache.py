from datetime import datetime
import json

from anime_credits_app import app_root


page_visits = {
    'staff' : [],
    'people' : []
}

def register_page_visit(category, mal_id):
    global page_visits
    for i, visit in enumerate(page_visits[category]):
        if visit['mal_id'] == mal_id:
            page_visits[category][i]["datetime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return

    page_visits[category].append({
        "mal_id" : mal_id,
         "datetime" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         })
    


def check_page_visit(category, mal_id):
    global page_visits
    for visit in page_visits[category]:
        if visit['mal_id'] == mal_id:
            return (True, datetime.strptime(visit['datetime'], '%Y-%m-%d %H:%M:%S'))
    return False


def save_page_visits():
    global page_visits

    with open(app_root / 'page_visits.json', 'w', encoding='utf-8') as f:
        json.dump(page_visits, f, indent=4, ensure_ascii=False)

def load_page_visits():
    global page_visits
    with open(app_root / 'page_visits.json', 'r', encoding='utf-8') as f:
        page_visits = json.load(f)