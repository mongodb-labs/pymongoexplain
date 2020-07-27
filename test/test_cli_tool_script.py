"""Script to test CLI functionality of pymongoexplain"""


import pymongo

import sys


client = pymongo.MongoClient(serverSelectionTimeoutMS=1000)
collection = client.db.get_collection("products")
collection.update_one({"quantity": 1057, "category": "apparel"},{"$set": {"reorder": True}})
