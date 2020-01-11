from pymongo import MongoClient
import pymongo
import numpy as np

import dotenv
import os

dotenv.load_dotenv()
ATLAS_KEY = os.getenv("KEY_ATLAS")


class ConectColl:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['Bycicle_Accidents']
        self.acc = self.db['Historical']
        self.pred = self.db['Prediction']
        self.no_damage = self.db['No_Damage']

    def add_doc(self, docu):
        self.acc.insert_one(docu)

# ---
    def add_doc_pred(self, docu):
        self.pred.insert_one(docu)
# ---

    def create(self, fecha, year, horario, festividad, tipo_accidente, lesividad, meteo, distrito, direccion, lon, lat):
        document = {
            'fecha': fecha,
            'year': year,
            'horario': horario,
            'festividad': festividad,
            'tipo_accidente': tipo_accidente,
            'lesividad': lesividad,
            'meteo': meteo,
            'distrito': distrito,
            'direccion': direccion,
            'localizacion': {
                'type': 'Point',
                'coordinates': [lon, lat]
            }
        }
        return self.add_doc(document)

# ----
    def create_pred(self, lon, lat, weight):
        document = {
            'Weights': weight,
            'localizacion': {
                'type': 'Point',
                'coordinates': [lon, lat]
            }
        }
        return self.add_doc_pred(document)
# ---


def geopoint(lon, lat):
    return {"type": "Point", "coordinates": [lon, lat]}


def submit_df(df):
    coll = ConectColl()
    df['Localizacion'] = np.vectorize(geopoint)(df['lon'], df['lat'])

    coll.no_damage.insert_many(df.to_dict('record'))
    coll.no_damage.create_index([('Localizacion', pymongo.GEOSPHERE)])
