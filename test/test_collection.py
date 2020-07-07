from pymongo import MongoClient
from pymongoexplain.explainable_collection import ExplainCollection
client = MongoClient(serverSelectionTimeoutMS=1000)
collection = client.db.products
explain = ExplainCollection(collection)
print(explain.update_one({"quantity": 1057, "category": "apparel"}, {"$set": {
    "reorder": True}}))