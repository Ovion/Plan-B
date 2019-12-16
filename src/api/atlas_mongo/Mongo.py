from pymongo import MongoClient
from ctes import MONGO, USER_ATLAS, KEY_ATLAS


class ConectColl:
    def __init__(self):
        self.client = MongoClient(MONGO.format(USER_ATLAS, KEY_ATLAS))
        self.db = self.client['Bycicle_Accidents']
        self.acc = self.db['History']
