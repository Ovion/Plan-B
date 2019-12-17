from pymongo import MongoClient

import dotenv
import os

dotenv.load_dotenv()
ATLAS_KEY = os.getenv("KEY_ATLAS")


class ConectColl:
    def __init__(self):
        self.client = MongoClient(ATLAS_KEY)
        self.db = self.client['Bycicle_Accidents']
        self.acc = self.db['Historical']

    def add_doc(self, docu):
        self.acc.insert_one(docu)

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
