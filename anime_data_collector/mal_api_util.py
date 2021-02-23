import requests
import json
from pathlib import Path




def check_resource_exists(resource_type:str, mal_id:int) -> bool:

    resource_endpoints = {
        'anime' : 'anime',
        'people' : 'people',
        'studios' : 'anime/producer'
    }
    request = f"https://myanimelist.net/{resource_endpoints[resource_type]}/{mal_id}"
    response = requests.get(request)
    return response.status_code != 404
    
    
    


def search_people_fallback(query):
    request = f"https://myanimelist.net/people.php?q={query}&cat=person"
    response = requests.get(request)
    

    mal_id = response.url.split('/')[-2]
    if not mal_id.isdigit():
        mal_id = response.url.split('/')[-1]

    return int(mal_id) if mal_id.isdigit() else None










    

