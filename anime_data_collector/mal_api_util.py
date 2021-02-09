import requests
import json
from pathlib import Path


def search_people_fallback(query):
    request = f"https://myanimelist.net/people.php?q={query}&cat=person"
    response = requests.get(request)

    print(response.url)
    

    mal_id = response.url.split('/')[-2]
    if not mal_id.isdigit():
        mal_id = response.url.split('/')[-1]


    return int(mal_id) if mal_id.isdigit() else None




    

