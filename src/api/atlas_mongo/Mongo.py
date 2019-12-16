from pymongo import MongoClient
from ctes import MONGO, USER_ATLAS, KEY_ATLAS


class ConectColl:
    def __init__(self):
        self.client = MongoClient(MONGO.format(USER_ATLAS, KEY_ATLAS))
        self.db = self.client['Bycicle_Accidents']
        self.acc = self.db['History']

    def add_doc(self, docu):
        self.acc.insert_one(docu)

    def create(self, year, lat, lon):
        document = {
            'year': year,
            'lat': lat,
            'lon': lon
        }
        return self.add_doc(document)
