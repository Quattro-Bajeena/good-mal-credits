import requests
import json, xmltodict
from xml.etree import ElementTree

endpoint = "https://cdn.animenewsnetwork.com/encyclopedia/api.xml?"


def save_to_json(data, file_name: str):
    root = ElementTree.fromstring(data)
    data = root.attrib
    data["anime"] = []

    for node in root.iter('item'):
        data["anime"].append(dict())
        for elem in node:
            # print(f"{elem.tag} - {elem.text}" )
            data["anime"][-1][elem.tag] = elem.text

    print(data)

    with open(file_name + ".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def download_report(skip : int, number : int, type, report_id = 155):
    ann_request = f"https://www.animenewsnetwork.com/encyclopedia/reports.xml?id={report_id}&type={type}&nskip={skip}&nlist={number}"
    response = requests.get(ann_request)
    save_to_json(response.content, f"anime_{skip}_{skip+number}")
