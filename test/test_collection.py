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
import subprocess
import os

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
    def setUp(self) -> None:
        self.logger = CommandLogger()
        self.client = MongoClient(serverSelectionTimeoutMS=1000,
                                 event_listeners=[self.logger])
        self.collection = self.client.db.products
        self.collection.insert_one({'x': 1})
        self.explain = ExplainCollection(self.collection)

    def _compare_command_dicts(self, ours, theirs):
        for key in ours.keys():
            self.assertEqual(ours[key], theirs[key])


    def test_update_one(self):
        self.collection.update_one({"quantity": 1057, "category": "apparel"},
                                 {"$set": {"reorder": True}})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.update_one({"quantity": 1057, "category": "apparel"},
                               {"$set": {"reorder": True}})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_update_many(self):
        self.collection.update_many({"quantity": 1057, "category": "apparel"},
                                  {"$set": {"reorder": True}})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.update_many({"quantity": 1057, "category": "apparel"},
                                {"$set": {"reorder": True}})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_distinct(self):
        self.collection.distinct("item.sku")
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.distinct("item.sku")
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_count_documents(self):
        self.collection.count_documents({"ord_dt": {"$gt": 10}})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.count_documents({"ord_dt": {"$gt": 10}})
        #self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_aggregate(self):
        self.collection.aggregate([{"$project": {"tags": 1}}, {"$unwind":
                                                                 "$tags"}],
                                None)
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.aggregate([{"$project": {"tags": 1}}, {"$unwind":
                                                                 "$tags"}], None)
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_delete_one(self):
        self.collection.delete_one({"status": "D"})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.delete_one({"status": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_delete_many(self):
        self.collection.delete_many({"status": "D"})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.delete_many({"status": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_watch(self):
        res = self.explain.watch()
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        self.collection.watch(pipeline=[{"$project": {"tags": 1}}],
                              batch_size=10, full_document="updateLookup")
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.watch(pipeline=[{"$project": {"tags": 1}}],
                                 batch_size=10, full_document="updateLookup")
        self.assertIn("queryPlanner", res["stages"][0]["$cursor"])
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find(self):
        for _ in self.collection.find(filter={"status": "D"}):
            pass
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find(filter={"status": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

        for _ in self.collection.find({}, limit=10):
            pass
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find({}, limit=10)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)



    def test_find_one(self):
        self.collection.find_one(projection=['a', 'b.c'])
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find_one(projection=['a', 'b.c'])
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

        self.collection.find_one(projection={'a': 1, 'b.c': 1})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find_one(projection={'a': 1, 'b.c': 1})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one_and_delete(self):
        self.collection.find_one_and_delete({"_id": "D"})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find_one_and_delete({"_id": "D"})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one_and_replace(self):
        self.collection.find_one_and_replace({'x': 1}, {'y': 1})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find_one_and_replace({'x': 1}, {'y': 1})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_find_one_and_update(self):
        self.collection.find_one_and_update({'_id': 665}, {'$inc': {'count': 1}, "$set": {'done': True}})
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.find_one_and_update({'_id': 665}, {'$inc': {'count': 1}, '$set': {'done': True}})
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_replace_one(self):
        self.collection.replace_one({'x': 1}, {'y': 1},
                               bypass_document_validation=True)
        last_logger_payload = self.logger.cmd_payload
        res = self.explain.replace_one({'x': 1}, {'y': 1}, bypass_document_validation=True)
        self.assertIn("queryPlanner", res)
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_estimated_document_count(self):
        self.collection.estimated_document_count()
        last_logger_payload = self.logger.cmd_payload
        self.explain.estimated_document_count()
        last_cmd_payload = self.explain.last_cmd_payload
        self._compare_command_dicts(last_cmd_payload, last_logger_payload)

    def test_cli_tool(self):
        script_path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "test_cli_tool_script.py")
        res = subprocess.run(["python3",  "-m", "pymongoexplain",
                              script_path], stdout = subprocess.PIPE)
        self.assertTrue(res.returncode == 0)
        self.assertNotEqual(res.stdout, "")

        res = subprocess.run(["python3",  "-m", "pymongoexplain",
                              script_path, "-h"], stdout = subprocess.PIPE)
        self.assertNotEqual(res.stdout, "")
        self.assertTrue(res.returncode == 0)

    def test_imports(self):
        from pymongoexplain import ExplainCollection
        from pymongoexplain import ExplainableCollection
        self.assertEqual(ExplainableCollection, ExplainCollection)

    def test_verbosity(self):
        res = self.explain.find({})
        self.assertNotIn("executionStats", res)
        self.assertNotIn("allPlansExecution", res.get("executionStats", []))
        self.explain = ExplainCollection(self.collection, verbosity="executionStats")
        res = self.explain.find({})
        self.assertIn("executionStats", res)
        self.assertNotIn("allPlansExecution", res["executionStats"])
        self.explain = ExplainCollection(self.collection, verbosity="allPlansExecution")
        res = self.explain.find({})
        self.assertIn("executionStats", res)
        self.assertIn("allPlansExecution", res["executionStats"])

    def test_comment(self):
        self.explain.find({})
        self.assertNotIn("comment", self.logger.cmd_payload)
        self.explain = ExplainCollection(self.collection, comment="comment")
        self.explain.find({})
        self.assertIn("comment", self.logger.cmd_payload)

if __name__ == '__main__':
    unittest.main()
