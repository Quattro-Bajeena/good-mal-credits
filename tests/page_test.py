import requests

url = "https://bettermalcredits.moe"



def trigger_page_downloads(category, mal_ids):
    length = len(mal_ids)
    for i, mal_id in enumerate(mal_ids):
        endpoint = f"{url}/{category}/{mal_id}"
        resp = requests.get(endpoint)
        print(f"{i}/{length} | {mal_id}:{resp.status_code}")


trigger_page_downloads("anime", range(50, 200))