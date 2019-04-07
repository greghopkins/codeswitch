import json
from pymongo import MongoClient
from geopy.geocoders import Nominatim
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
                if "location" in query:
                    sphere = query["location"]
                    query["location"] = {
                        "$geoWithin": {
                            "$centerSphere": [
                                sphere['geojson']['coordinates'],
                                float(sphere['radius'])/3963.2
                            ]
                        }
                    }

                value_types = []
                if "values" in query:
                    value_types = query["values"]
                    query["values"] = {"$in": value_types}
                    agg_query = [
                        {"$match": query},
                        {"$addFields": {
                            "values_matched": {
                                "$setIntersection": ["$values", value_types]
                            }
                        }}
                    ]

                else:
                    agg_query = [
                        {"$match": query},
                    ]

                print("Executing query:\n{}".format(json.dumps(agg_query)))
                for resp in coll.aggregate(agg_query):
                    resp['_id'] = str(resp['_id'])
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


class Locator(object):
    def __init__(self):
        self.geolocator = Nominatim(user_agent="hidden_gems_v1")

    def locate(self, address_dict):
        return self.geolocator.geocode("{street1}, {city}, {state}, {zip}".format(**address_dict))

    def to_geojson(self, location):
        return {
            "type": "Point",
            "coordinates": [location.longitude, location.latitude]
        }
