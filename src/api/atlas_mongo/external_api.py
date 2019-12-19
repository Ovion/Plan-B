
from googlemaps import Client as GoogleMaps
import os
from dotenv import load_dotenv


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
