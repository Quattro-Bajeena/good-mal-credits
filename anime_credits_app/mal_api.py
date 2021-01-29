from anime_credits_app import anime_db_config as conf
from jikanpy import Jikan
from pathlib import Path
import json
import time
import functools

jikan = Jikan()

second_limit_max = 2
minute_limit_max = 30

second_limit = 2
minute_limit = 30

last_request = time.time()


def rate_limiter(func_with_api_call):
    @functools.wraps(func_with_api_call)
    def wrapper(*args, **kwargs):
        global second_limit, second_limit_max, minute_limit, minute_limit_max
        global last_request

        if time.time() - last_request > 1:
            second_limit = second_limit_max
        if time.time() - last_request > 60:
            minute_limit = minute_limit_max

        if second_limit == 0:
            print("hit second rate limit")
            time.sleep(1)
        if minute_limit == 0:
            print("hit minute rate limit")
            time.sleep(60 - (time.time() - last_request))

        second_limit -= 1
        minute_limit -= 1

        last_request = time.time()

        return func_with_api_call(*args, **kwargs)

    return wrapper

@rate_limiter
def id_from_search(type: str, query: str) -> int:
    results = jikan.search(search_type=type, query=query, page=1)

    return int(results["results"][0]["mal_id"])

@rate_limiter
def search_options(type: str, query: str):
    results = jikan.search(search_type=type, query=query)
    options = []
    first_5 = results["results"][0:5]

    for mal_result in first_5:
        result = {}
        attributes_to_copy = ["mal_id", "title", "url", "image_url"]
        for attr in attributes_to_copy:
            result[attr] = mal_result[attr]
        options.append(result)

    return options

# STAFF
@rate_limiter
def get_staff_api(mal_id) -> list:
    characters_staff = jikan.anime(mal_id, extension="characters_staff")
    return {"mal_id": mal_id, "staff": characters_staff["staff"]}


def save_staff(mal_id, staff: list):
    with open(conf.staff_folder / Path(f"staff-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(staff, f, indent=4, ensure_ascii=False)

# PEOPLE
@rate_limiter
def get_person_api(mal_id) -> dict:
    mal_person = jikan.person(mal_id)
    person = {}
    attributes_to_copy = ["mal_id", "url", "image_url", "name", "given_name", "family_name",
                          "birthday", "member_favorites",
                          "voice_acting_roles", "anime_staff_positions"]

    for attr in attributes_to_copy:
        person[attr] = mal_person[attr]
    return person


def save_person(person):
    mal_id = person["mal_id"]
    with open(conf.people_folder / Path(f"person-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(person, f, indent=4, ensure_ascii=False)

# ANIME
@rate_limiter
def get_anime_api(mal_id: int):
    anime_mal = jikan.anime(mal_id)
    anime = {}
    attributes_to_copy = ["mal_id", "url", "image_url", "title", "title_english", "title_japanese",
                          "type", "source", "episodes", "status", "aired",
                          "score", "scored_by", "rank", "popularity", "members", "favorites",
                          "premiered",
                          "studios"]
    for attr in attributes_to_copy:
        anime[attr] = anime_mal[attr]
    return anime


def save_anime(anime: dict):
    mal_id = anime["mal_id"]
    with open(conf.anime_folder / Path(f"anime-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(anime, f, indent=4, ensure_ascii=False)


#GENERAL

def check_file(resource_type, mal_id : int) -> bool:
    folder = conf.resource_types[resource_type]
    files = folder.rglob('*.json')

    for file in files:
        file_id = int(file.stem.split('-')[1])
        if file_id == mal_id:
            return True
    return False
    


def get_data_file(resource_type, id: int):
    folder = conf.resource_types[resource_type]

    files = folder.rglob('*.json')
    for file in files:
        file_id = int(file.stem.split('-')[1])
        if file_id == id:
            with open(file, 'r') as f:
                return json.load(f)
    return None



# save_person(get_person_api(2))
# save_staff(1, get_staff_api(1))
# print(get_data_file("anime", 1))
# save_anime(get_anime_api(1))

# id_from_search("anime", "attack on titan")
# search_options("anime", "attack on titan")

if __name__ == "__main__":
    id = id_from_search("anime", "guren lagann")
    person = get_anime_api(id)
    save_anime(person)
    print(second_limit, minute_limit)
