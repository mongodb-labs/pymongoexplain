# Copyright 2020-present MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pymongo import MongoClient
from pymongoexplain.explainable_collection import ExplainCollection
import unittest


class TestExplainableCollection(unittest.TestCase):
    def test_update_one(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        try:
            explain.update_one({"quantity": 1057, "category": "apparel"},
                               {"$set": {"reorder": True}})
        except:
            assert False

    def test_update_many(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        try:
            explain.update_many({"quantity": 1057, "category": "apparel"},
                               {"$set": {"reorder": True}})
        except:
            assert False

    def test_distinct(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        try:
            explain.distinct("item.sku")
        except:
            assert False

    def test_count_documents(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        try:
            explain.count_documents({"ord_dt": { "$gt": 10}})
        except:
            assert False

    def test_aggregate(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        try:
            explain.aggregate([{"$project": {"tags": 1 }}, {"$unwind": "$tags"},
                               {"$group": {"_id": "$tags", "count":
                                   {"$sum" : 1 } }}], None)
        except:
            assert False


if __name__ == '__main__':
    unittest.main()