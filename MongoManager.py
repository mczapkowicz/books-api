from pymongo import MongoClient
from flask import current_app

class MongoManager:
    __instance = None

    @staticmethod
    def getInstance():
        if MongoManager.__instance == None:
            MongoManager()
        return MongoManager.__instance

    def __init__(self):
        if MongoManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoManager.__instance = MongoClient(current_app.config['DB_URL'])