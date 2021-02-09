from jikanpy import Jikan, APIException
from pathlib import Path
import json
import time
import functools

# this is relative import, it will only work if this module is imported from somewhre else
#  like import anime_data_collector.mal_api
# this wont work if I it's run like python mal_api.py, 
# for that you have to do absolute import, like import anime_db_config as config
# but that won't do if you import this package

import anime_data_collector.anime_db_config as config




#print("anieme mal", Path(__name__).resolve())

jikan = Jikan()

second_limit_max = 2
minute_limit_max = 30

second_limit = 2
minute_limit = 15

last_request = time.time()


def rate_limiter(func_with_api_call):
    @functools.wraps(func_with_api_call)
    def wrapper(*args, **kwargs):
        global second_limit, second_limit_max, minute_limit, minute_limit_max
        global last_request

        # print(f"RATE LIMITER: {second_limit} / {minute_limit}: {round(time.time() - last_request, 3)}")

        # if second_limit <= 0:
        #     print("hit SECOND rate LIMIT")
        #     time.sleep(4)
        # if minute_limit <= 0:
        #     print("hit MINUTE rate LIMIT")
        #     #time.sleep(60 - (time.time() - last_request))
        #     time.sleep(70)

        # if time.time() - last_request > 3:
        #     second_limit = second_limit_max
        #     print("RESTORED SECOND LIMIT")
        # if time.time() - last_request > 70:
        #     minute_limit = minute_limit_max
        #     print("RESTORE MINUTE LIMIT")

        # second_limit -= 1
        # minute_limit -= 1
        
        # last_request = time.time()

        time.sleep(4)
        return func_with_api_call(*args, **kwargs)

    return wrapper

@rate_limiter
def id_from_search(type: str, query: str) -> int:
    results = jikan.search(search_type=type, query=query, page=1)

    return int(results["results"][0]["mal_id"])

@rate_limiter
def search_options(q_type: str, query: str, number : int = 0):
    results_api = jikan.search(search_type=q_type, query=query)
    options = []

    results = results_api["results"]

    if number:
        results = results[0:number]

    
    attributes_to_copy = ["mal_id", "url", "image_url"]
    if q_type == "anime":
        attributes_to_copy.append("title")
    if q_type == "people":
        attributes_to_copy.append("name")

    for mal_result in results:
        result = {}
        for attr in attributes_to_copy:
            result[attr] = mal_result[attr]
        options.append(result)

    

    return options

# CHARACTERS AND STAFF
@rate_limiter
def get_characters_staff_api(mal_id : int) -> list:
    characters_staff = jikan.anime(mal_id, extension="characters_staff")
    return {"mal_id": mal_id, "characters":characters_staff['characters'], "staff": characters_staff["staff"]}


def save_characters_staff(characters_staff: list):
    mal_id = characters_staff['mal_id']
    with open(config.characters_staff_folder / Path(f"characters_staff-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(characters_staff, f, indent=4, ensure_ascii=False)


# CHARACTER
def get_character_api(mal_id : int) -> dict:
    mal_character = jikan.character(mal_id)
    character = {}
    attributes_to_copy = [
        'mal_id', 'url', 'name', 'name_kanji', 'nicknames', 'member_favorites',
        'image_url',
        'animeography', 'mangaography', 'voice_actors'
    ]
    for attr in attributes_to_copy:
        character[attr] = mal_character[attr]

    return character

def save_character(character : dict):
    mal_id = character['mal_id']
    with open(config.characters_folder / Path(f"character-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(character, f, indent=4, ensure_ascii=False)

# PEOPLE
@rate_limiter
def get_person_api(mal_id:int) -> dict:
    mal_person = jikan.person(mal_id)
    person = {}
    attributes_to_copy = [
        "mal_id", "url", "image_url", "name", "given_name", "family_name",
        "birthday", "member_favorites",
        "voice_acting_roles", "anime_staff_positions", "published_manga"
        ]

    for attr in attributes_to_copy:
        person[attr] = mal_person[attr]
    return person


def save_person(person):
    mal_id = person["mal_id"]
    with open(config.people_folder / Path(f"person-{mal_id}.json"), 'w', encoding='utf-8') as f:
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
    with open(config.anime_folder / Path(f"anime-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(anime, f, indent=4, ensure_ascii=False)


# MANGA
@rate_limiter
def get_manga_api(mal_id:int):
    manga_mal = jikan.manga(mal_id)
    manga = {}
    attributes_to_copy = ["mal_id", "url", "image_url", "title", "title_english", "title_japanese",
                          "type", "volumes", "chapters", "status","publishing" ,"published",
                          "score", "scored_by", "rank", "popularity", "members", "favorites",
                          "authors", "serializations"]
    for attr in attributes_to_copy:
        manga[attr] = manga_mal[attr]
    return manga

def save_manga(manga: dict):
    mal_id = manga["mal_id"]
    with open(config.manga_folder / Path(f"manga-{mal_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(manga, f, indent=4, ensure_ascii=False)

#GENERAL

def check_file(resource_type, mal_id : int) -> bool:
    folder = config.resource_types[resource_type]
    files = folder.rglob('*.json')

    for file in files:
        file_id = int(file.stem.split('-')[1])
        if file_id == mal_id:
            return True
    return False
    


def get_data_file(resource_type, id: int):
    folder = config.resource_types[resource_type]

    files = folder.rglob('*.json')
    for file in files:
        file_id = int(file.stem.split('-')[1])
        if file_id == id:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None


# checks if resource is already downloaded, if not downlaods and saves it
# if it is, it just loads it from file
def get_resource(resource_type : str, mal_id : int, use_cached = True):

    get_functions = {
        'anime' : get_anime_api,
        'people' : get_person_api,
        'characters_staff' : get_characters_staff_api,
        'characters' : get_character_api,
        'manga' : get_manga_api
    }

    save_functions = {
        'anime' : save_anime,
        'people' : save_person,
        'characters_staff' : save_characters_staff,
        'characters' : save_character,
        'manga' : save_manga
    }

    

    if use_cached and check_file( resource_type, mal_id):
        resource = get_data_file(resource_type, mal_id)
    else:
        try:
            resource = get_functions[resource_type](mal_id)
        except APIException as e:
            print("RESOURCE COULDN'T BE OPTAINED FROM MAL")
            print(e)
            return None
        save_functions[resource_type](resource)

    return resource



