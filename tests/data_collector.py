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


save_character(140810)



