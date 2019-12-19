import requests
from googlemaps import Client as GoogleMaps
import os
from dotenv import load_dotenv
import json
import re


def get_coord_dir(direction):
    load_dotenv()

    G_KEY = os.getenv("KEY_GOOGLE")
    gmaps = GoogleMaps(G_KEY)
    geocode_result = gmaps.geocode(direction)
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        return lat, lon
    except:
        lat = None
        lon = None
        print('At least I tried')


def get_weather_day():
    load_dotenv()

    A_KEY = os.getenv("KEY_AIR")
    url = f"http://api.airvisual.com/v2/city?city=Madrid&state=Madrid&country=Spain&key={A_KEY}"
    payload, files, headers = {}, {}, {}

    response = requests.request(
        "GET", url, headers=headers, data=payload, files=files)
    jeison = json.loads(response.text)
    weather = jeison['data']['current']['weather']['ic']
    w_num = re.sub(r"[a-z]", "", weather)
    dict_weather = {
        '01': 'Despejado', '02': 'Despejado', '03': 'Despejado', '04': 'Despejado',
        '09': 'Lluvia', '10': 'Lluvia', '11': 'Lluvia', '13': 'Lluvia',
        '50': 'Niebla'}
    w = dict_weather[w_num]
    date = jeison['data']['current']['weather']['ts']
    d = re.findall(r"\d+-\d+-\d+", date)[0]

    return w, d
