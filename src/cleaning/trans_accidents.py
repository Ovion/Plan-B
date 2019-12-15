
import pandas as pd
from googlemaps import Client as GoogleMaps
import os
from dotenv import load_dotenv

import functions.trans_fn as fnt

load_dotenv()

print('Transforming data...')
bici_19 = pd.read_csv('input/clean_data/AB_19.csv')
bici_18 = pd.read_csv('input/clean_data/AB_18.csv')
bici_17 = pd.read_csv('input/clean_data/AB_17.csv')
cal = pd.read_csv('input/raw_data/bicicletas/calendario.csv',
                  encoding='latin_1', sep=';')

bici = pd.concat([bici_19, bici_18, bici_17], ignore_index=True)
bici = fnt.horario(bici)

cal = fnt.clean_calendar(cal)

bici = bici.merge(cal, how='left', on='dia')
bici = fnt.prepare_to_google(bici)
print('Done')
print('Saving data in: input/clean_data/bici_woCoor.csv')
bici.to_csv('input/clean_data/bici_woCoor.csv')
print('Done')

print('Getting coordinates...')
G_KEY = os.getenv("KEY_GOOGLE")
gmaps = GoogleMaps(G_KEY)

for i in range(len(bici)):
    geocode_result = gmaps.geocode(
        bici.iat[i, bici.columns.get_loc('direccion')])
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        bici.iat[i, bici.columns.get_loc('lat')] = lat
        bici.iat[i, bici.columns.get_loc('lon')] = lon
    except:
        lat = None
        lon = None
        print('At least I tried')
print('Done')

print('Saving .csv in: input/clean_data/bici.csv')
bici.to_csv('input/clean_data/bici.csv')
print('Done')
