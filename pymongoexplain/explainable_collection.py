import pymongo
from json import dumps


class BaseCommand():
    def __init__(self, dictionary):
        self.dictionary = self.convert_to_camelcase(dictionary)

    def convert_to_camelcase(self, d: dict) -> dict:
        ret = dict()
        for key in d.keys():
            if "_" in key:
                new_key = key.split("_")[0] + ''.join(
                    [i.capitalize() for i in key.split("_")[1:]])
                ret[new_key] = d[key]
            else:
                ret[key] = d[key]
        return ret

    def get_SON(self):
        return self.dictionary


class UpdateCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, filter, update,
                 **kwargs):
        self.dictionary = {"update": collection.name,
                           "updates": [{"q": filter, "u": update}]}
        for key, value in kwargs:
            self.dictionary["updates"][0][key] = value
        super(UpdateCommand, self).__init__(self.dictionary)


class ExplainCollection():
    def __init__(self, collection):
        self.collection = collection

    def update_one(self, filter, update):
        command = UpdateCommand(self.collection, filter, update)
        print({"explain": command.get_SON(), "verbosity": "queryPlanner"})
        return self.collection.database.command(
            {"explain": command.get_SON(), "verbosity": "queryPlanner"})


from pymongo import MongoClient

client = MongoClient(serverSelectionTimeoutMS=1000)
collection = client.db.products
explain = ExplainCollection(collection)
print(explain.update_one({"quantity": 1057, "category": "apparel"}, {"$set": {
    "reorder": True}}))
