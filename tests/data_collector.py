import sys
from os import path
from pathlib import Path
import json

# print(path.abspath(__file__))
# print(path.dirname(path.abspath(__file__)))
# print(path.dirname(path.dirname(path.abspath(__file__))))

# print(Path(__file__).resolve().parent.parent)

#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(str(Path(__file__).resolve().parent.parent))


import anime_data_collector as adc

test_folder = Path(__file__).parent
adc.anime_db_config.config_database(test_folder)


# query = "patlabor"
# results = adc.mal.search_options("anime", query, 5)


# with open( test_folder / f"search-{query}.json", 'w', encoding='utf-8') as f:
#     json.dump(results, f, indent=4, ensure_ascii=False)


def download_person(id):
    person = adc.mal.get_person_api(7998)

    with open( test_folder / f"person-{id}.json", 'w', encoding='utf-8') as f:
        json.dump(person, f, indent=4, ensure_ascii=False)


def search_people(query):
    results = adc.mal.search_options('people', query, None)

    with open( test_folder / f"search-test.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

def save_character(mal_id):
    character = adc.mal.get_character_api(mal_id)

    with open( test_folder / f"character-test.json", 'w', encoding='utf-8') as f:
            json.dump(character, f, indent=4, ensure_ascii=False)


def studio_test(mal_id):
    studio = adc.mal.get_studio_api(1)
    adc.mal.save_studio(studio)

# print(adc.util.check_resource_exists('anime', 1))
# print(adc.util.check_resource_exists('anime', 2))
# print(adc.util.check_resource_exists('people', 99999))
# print(adc.util.check_resource_exists('studios', 803))



