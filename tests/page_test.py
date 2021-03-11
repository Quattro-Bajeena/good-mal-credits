import requests

url = "https://bettermalcredits.moe"



def trigger_page_downloads(category, mal_ids):
    length = len(mal_ids)
    for i, mal_id in enumerate(mal_ids):
        endpoint = f"{url}/{category}/{mal_id}"
        resp = requests.get(endpoint)
        print(f"{i+1}/{length} | {mal_id}:{resp.status_code}")


trigger_page_downloads("people", range(1, 1000))