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

import logging

from pymongo import monitoring
from bson import Timestamp

class CommandLogger(monitoring.CommandListener):
    def started(self, event):
        self.cmd_payload = event.command
        print(self.cmd_payload)

class TestExplainableCollection(unittest.TestCase):
    def test_update_one(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.update_one({"quantity": 1057, "category": "apparel"},
                               {"$set": {"reorder": True}})
        self.assertIn("queryPlanner", res)

    def test_update_many(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.update_many({"quantity": 1057, "category": "apparel"},
                                {"$set": {"reorder": True}})
        self.assertIn("queryPlanner", res)

    def test_distinct(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.distinct("item.sku")
        self.assertIn("queryPlanner", res)

    def test_count_documents(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.count_documents({"ord_dt": {"$gt": 10}})
        self.assertIn("queryPlanner", res)

    def test_aggregate(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.aggregate([{"$project": {"tags": 1}}, {"$unwind":
                                                                 "$tags"}], None)
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])

    def test_delete_one(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.delete_one({"status": "D"})
        self.assertIn("queryPlanner", res)

    def test_delete_many(self):
        client = MongoClient(serverSelectionTimeoutMS=1000)
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.delete_many({"status": "D"})
        self.assertIn("queryPlanner", res)

    def test_watch(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        res = explain.watch()
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        collection.watch(pipeline=[{"$project": {"tags": 1}}],
                               batch_size=10, full_document="updateLookup")
        res_exp = explain.watch(pipeline=[{"$project": {"tags": 1}}],
                            batch_size=10, full_document="updateLookup")
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        last_cmd_payload = explain.last_cmd_payload
        for key in last_cmd_payload.keys():
            assert last_cmd_payload[key] == logger.cmd_payload[key]


if __name__ == '__main__':
    unittest.main()
