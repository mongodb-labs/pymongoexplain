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
                 kwargs):
        self.dictionary = {"update": collection.name,
                           "updates": [{"q": filter, "u": update}]}
        for key, value in kwargs.items():
            self.dictionary["updates"][0][key] = value
        super(UpdateCommand, self).__init__(self.dictionary)

class DistinctCommand(BaseCommand):
    def __init__(self, key, collection: pymongo.collection, filter, session,
                 kwargs):
        self.dictionary = {"distinct": collection.name, "key": key, "query":
            filter}
        for key, value in kwargs.items():
            self.dictionary[key] = value
        super(UpdateCommand, self).__init__(self.dictionary)

class AggregateCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, pipeline, kwargs):
        self.dictionary = {"aggregate": collection.name, "pipeline": pipeline,
                           "query": filter}
        for key, value in kwargs.items():
            self.dictionary[key] = value
        super(UpdateCommand, self).__init__(self.dictionary)

class CountCommand(BaseCommand):
    def __init__(self, collection: pymongo.collection, filter,
                 kwargs):
        self.dictionary = {"count": collection.name,
                           "query": filter}
        for key, value in kwargs.items():
            self.dictionary[key] = value
        super(UpdateCommand, self).__init__(self.dictionary)

class ExplainCollection():
    def __init__(self, collection):
        self.collection = collection

    def _explain_command(self, command):
        print({"explain": command.get_SON(), "verbosity": "queryPlanner"})
        return self.collection.database.command(
            {"explain": command.get_SON(), "verbosity": "queryPlanner"})

    def update_one(self, filter, update, **kwargs):
        kwargs["multi"] = False
        command = UpdateCommand(self.collection, filter, update, kwargs)
        return self._explain_command(command)

    def update_many(self, filter, update, **kwargs):
        kwargs["multi"] = True
        command = UpdateCommand(self.collection, filter, update, kwargs)
        return self._explain_command(command)

    def distinct(self, key, filter=None, session=None, **kwargs):
        command = DistinctCommand(key, self.collection, filter, session, kwargs)
        return self._explain_command(command)

    def aggregate(self, pipeline, session=None, **kwargs):
        command = AggregateCommand(key, self.collection, filter, session, kwargs)
        return self._explain_command(command)


