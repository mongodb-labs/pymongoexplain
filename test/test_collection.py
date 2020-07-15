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

import unittest

from pymongo import MongoClient
from pymongo import monitoring
from bson import Timestamp
from bson.son import SON

from pymongoexplain.explainable_collection import ExplainCollection, Document


class CommandLogger(monitoring.CommandListener):
    def __init__(self):
        self.cmd_payload = {}
    def started(self, event):
        self.cmd_payload = event.command

    def succeeded(self, event):
        pass

    def failed(self, event):
        pass

class TestExplainableCollection(unittest.TestCase):
    def _compare_command_dicts(self, ours, theirs):
        for key in ours.keys():
            if isinstance(ours[key], dict) or isinstance(ours[key], SON):
                self._compare_command_dicts(ours[key], theirs[key])
            elif isinstance(ours[key], list):
                for i, j in zip(ours[key], theirs[key]):
                    if isinstance(i, dict) or isinstance(i,
                                                                 SON):
                        self._compare_command_dicts(i, j)
                    else:
                        assert i == j
            else:
                assert ours[key] == theirs.get(key, None)


    def test_update_one(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.update_one({"quantity": 1057, "category": "apparel"},
                                 {"$set": {"reorder": True}})
        last_logger_payload = logger.cmd_payload
        res = explain.update_one({"quantity": 1057, "category": "apparel"},
                               {"$set": {"reorder": True}})
        print(res)
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_update_many(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.update_many({"quantity": 1057, "category": "apparel"},
                                  {"$set": {"reorder": True}})
        last_logger_payload = logger.cmd_payload
        res = explain.update_many({"quantity": 1057, "category": "apparel"},
                                {"$set": {"reorder": True}})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_distinct(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.distinct("item.sku")
        last_logger_payload = logger.cmd_payload
        res = explain.distinct("item.sku")
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_count_documents(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.count_documents({"ord_dt": {"$gt": 10}})
        last_logger_payload = logger.cmd_payload
        res = explain.count_documents({"ord_dt": {"$gt": 10}})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_aggregate(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.aggregate([{"$project": {"tags": 1}}, {"$unwind":
                                                                 "$tags"}],
                                None)
        last_logger_payload = logger.cmd_payload
        res = explain.aggregate([{"$project": {"tags": 1}}, {"$unwind":
                                                                 "$tags"}], None)
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_delete_one(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.delete_one({"status": "D"})
        last_logger_payload = logger.cmd_payload
        res = explain.delete_one({"status": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_delete_many(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.delete_many({"status": "D"})
        last_logger_payload = logger.cmd_payload
        res = explain.delete_many({"status": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

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
        last_logger_payload = logger.cmd_payload
        res = explain.watch(pipeline=[{"$project": {"tags": 1}}],
                            batch_size=10, full_document="updateLookup")
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        for _ in collection.find(filter={"status": "D"}):
            pass
        last_logger_payload = logger.cmd_payload
        res = explain.find(filter={"status": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.find_one()
        last_logger_payload = logger.cmd_payload
        res = explain.find_one()
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one_and_delete(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.find_one_and_delete({"_id": "D"})
        last_logger_payload = logger.cmd_payload
        res = explain.find_one_and_delete({"_id": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one_and_replace(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.find_one_and_replace({'x': 1}, {'y': 1})
        last_logger_payload = logger.cmd_payload
        res = explain.find_one_and_replace({'x': 1}, {'y': 1})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one_and_update(self):
        logger = CommandLogger()
        client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[
            logger])
        collection = client.db.products
        explain = ExplainCollection(collection)
        collection.find_one_and_update({'_id': 665}, {'$inc': {'count': 1}, "$set": {'done': True}})
        last_logger_payload = logger.cmd_payload
        res = explain.find_one_and_update({'_id': 665}, {'$inc': {'count': 1}, '$set': {'done': True}})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)


if __name__ == '__main__':
    unittest.main()
