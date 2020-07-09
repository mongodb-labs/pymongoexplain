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


import pymongo
from bson.son import SON


class BaseCommand():
    def __init__(self, dictionary):
        self.dictionary = self.convert_to_camelcase(dictionary)

    def convert_to_camelcase(self, d: dict) -> dict:
        ret = dict()
        for key in d.keys():
            if d[key] is None:
                continue
            if "_" in key:
                new_key = key.split("_")[0] + ''.join(
                    [i.capitalize() for i in key.split("_")[1:]])
                ret[new_key] = d[key]
            else:
                ret[key] = d[key]
        return ret

    def get_SON(self):
        cmd = SON([(self.command_name, self.collection)])
        cmd.update(self.dictionary)
        return cmd


class UpdateCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, filter, update,
                 kwargs):
        super().__init__(kwargs)
        self.command_name = "update"
        self.collection = collection.name
        return_dictionary =  {"updates":[{"q": filter, "u": update}]}
        for key, value in self.dictionary.items():
            if key == "bypassDocumentValidation":
                return_dictionary[key] = value
            else:
                return_dictionary["updates"][0][key] = value
        self.dictionary = return_dictionary


class DistinctCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, key, filter, session,
                 kwargs):
        self.command_name = "distinct"
        self.collection = collection.name
        self.dictionary = {"key": key, "query": filter}
        for key, value in kwargs.items():
            self.dictionary[key] = value
        super().__init__(self.dictionary)


class AggregateCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, pipeline, session,
                 kwargs):
        self.command_name = "aggregate"
        self.collection = collection.name
        self.dictionary = {"pipeline": pipeline, "cursor": {}}
        for key, value in kwargs.items():
            self.dictionary[key] = value
        super().__init__(self.dictionary)


class CountCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, filter,
                 kwargs):
        self.command_name = "count"
        self.collection = collection.name
        self.dictionary = {"query": filter}
        for key, value in kwargs.items():
            self.dictionary[key] = value
        super().__init__(self.dictionary)


class DeleteCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, filter,
                 limit, collation, kwargs):
        super().__init__(kwargs)
        self.command_name = "delete"
        self.collection = collection.name
        return_dictionary = {"deletes": [{"q": filter, "limit": limit,
                                         "collation": collation}]}

        for key, value in self.dictionary.items():
            return_dictionary[key] = value
        self.dictionary = return_dictionary


class ExplainCollection():
    def __init__(self, collection):
        self.collection = collection

    def _explain_command(self, command):
        explain_command = SON([("explain", command.get_SON())])
        explain_command["verbosity"] = "queryPlanner"
        return self.collection.database.command(explain_command)

    def update_one(self, filter, update, upsert=False,
                   bypass_document_validation=False,
                   collation=None, array_filters=None, hint=None,
                   session=None, **kwargs):
        kwargs["multi"] = False
        kwargs["upsert"] = upsert
        kwargs["bypass_document_validation"] = bypass_document_validation
        kwargs["collation"] = collation
        kwargs["array_filters"] = array_filters
        kwargs["hint"] = hint
        kwargs["session"] = session
        command = UpdateCommand(self.collection, filter, update, kwargs)
        return self._explain_command(command)

    def update_many(self, filter, update, **kwargs):
        kwargs["multi"] = True
        command = UpdateCommand(self.collection, filter, update, kwargs)
        return self._explain_command(command)

    def distinct(self, key, filter=None, session=None, **kwargs):
        command = DistinctCommand(self.collection, key, filter, session, kwargs)
        return self._explain_command(command)

    def aggregate(self, pipeline, session=None, **kwargs):
        command = AggregateCommand(self.collection, pipeline, session,
                                   kwargs)
        return self._explain_command(command)

    def count_documents(self, filter, session=None, **kwargs):
        command = CountCommand(self.collection, filter,kwargs)
        return self._explain_command(command)


    def delete_one(self, filter, collation=None, session=None, **kwargs):
        limit = 1
        command = DeleteCommand(self.collection, filter, limit, collation,
                                kwargs)
        return self._explain_command(command)

    def delete_many(self, filter, collation=None, session=None, **kwargs):
        limit = 0
        command = DeleteCommand(self.collection, filter, limit, collation,
        kwargs)
        return self._explain_command(command)
