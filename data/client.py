from pymongo import MongoClient
from random import randint

class Session(object):
    def __init__(self, name='default'):
        self._client = MongoClient(
            'mongodb+srv://ksapp:codeswitch123db1@codeswitch-hhgf3.mongodb.net/test?retryWrites=true'
        )
        self.db = self._client.get_database(name)

    def count(self):
        return randint(1,3)

    def query(self, **collections):
        resp_dict = {}
        for collection_name, queries in collections.items():
            coll = self.db.get_collection(collection_name)
            resp_dict[collection_name] = []
            for query in queries:
                for resp in coll.find(query):
                    resp_dict[collection_name].append(resp)

        return resp_dict

    def sample(self, *collections):
        resp_dict = {}
        for collection_name in collections:
            coll = self.db.get_collection(collection_name)
            resp_dict[collection_name] = []
            for resp in list(coll.aggregate([{"$sample": {"size": self.count()}}])):
                resp_dict[collection_name].append(resp)

        return resp_dict

    def insert(self, **collections):
        inserted = []
        for collection_name, docs in collections.items():
            coll = self.db.get_collection(collection_name)
            for doc in docs:
                inserted.append(coll.insert_one(doc))

        return inserted

    def __del__(self):
        self._client.close()
