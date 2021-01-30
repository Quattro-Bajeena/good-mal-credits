import requests
import json
from xml.etree import ElementTree
from pathlib import Path

import anime_data_collector.anime_db_config as config




def save_report_to_json(data, file_name: str):
    root = ElementTree.fromstring(data)
    data = root.attrib
    data["anime"] = []

    for node in root.iter('item'):
        data["anime"].append(dict())
        for elem in node:
            # print(f"{elem.tag} - {elem.text}" )
            data["anime"][-1][elem.tag] = elem.text

    print(data)

    with open(config.anime_folder / Path(file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def download_report(skip: int, number: int, type, report_id=155):
    ann_request = f"https://www.animenewsnetwork.com/encyclopedia/reports.xml?id={report_id}&type={type}&nskip={skip}&nlist={number}"
    response = requests.get(ann_request)
    save_report_to_json(response.content, f"anime_{skip}_{skip + number}")


def save_details_json(data, file_name):


    # with open(anime_folder / Path(file_name + ".xml"), 'w', encoding='utf-8') as f:
    #     f.write(data)
    pass


def download_details(id, type="anime"):
    id = 4658
    type = "anime"
    ann_request = f"https://cdn.animenewsnetwork.com/encyclopedia/api.xml?{type}={id}"

    #response = requests.get(ann_request)
    #print(response.text)
    file = open(config.anime_folder / "anime-4658.xml", encoding='utf-8')

    save_details_json(file.read(), f"{type}-{id}")


download_details(4658)
