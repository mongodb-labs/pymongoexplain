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


"""Classes for generating command payloads."""


from typing import Union

from bson.son import SON
from pymongo.collection import Collection

Document = Union[dict, SON]

class BaseCommand():
    def __init__(self, command_name, collection):
        self.command_document = {}
        self.command_name = command_name
        self.collection = collection

    def convert_to_camelcase(self, d):
        if not isinstance(d, dict):
            return d
        ret = dict()
        for key in d.keys():
            if d[key] is None:
                continue
            new_key = key
            if "_" in key and key[0] != "_":
                new_key = key.split("_")[0] + ''.join(
                    [i.capitalize() for i in key.split("_")[1:]])
            if isinstance(d[key], list):
                ret[new_key] = [self.convert_to_camelcase(i) for i in d[key]]
            elif isinstance(d[key], dict):
                ret[new_key] = self.convert_to_camelcase(d[key])
            else:
                ret[new_key] = d[key]
        return ret

    def get_SON(self):
        cmd = SON([(self.command_name, self.collection)])
        cmd.update(self.command_document)
        return cmd


class UpdateCommand(BaseCommand):
    def __init__(self, collection: Collection, filter, update,
                 kwargs):
        super().__init__("update", collection.name)
        return_dictionary =  {"updates":[{"q": filter, "u": update}]}
        for key, value in self.command_document.items():
            if key == "bypassDocumentValidation":
                return_dictionary[key] = value
            else:
                return_dictionary["updates"][0][key] = value
        self.command_document = return_dictionary
        self.command_document = self.convert_to_camelcase(self.command_document)



class DistinctCommand(BaseCommand):
    def __init__(self, collection: Collection, key, filter, session,
                 kwargs):
        super().__init__("distinct", collection.name)
        self.command_document = {"key": key, "query": filter}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = self.convert_to_camelcase(self.command_document)


class AggregateCommand(BaseCommand):
    def __init__(self, collection: Collection, pipeline, session,
                 cursor_options,
                 kwargs):
        super().__init__("aggregate", collection.name)
        self.command_document = {"pipeline": pipeline, "cursor": cursor_options}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = self.convert_to_camelcase(self.command_document)


class CountCommand(BaseCommand):
    def __init__(self, collection: Collection, filter,
                 kwargs):
        super().__init__("count", collection.name)
        self.command_document = {"query": filter}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = self.convert_to_camelcase(self.command_document)



class FindCommand(BaseCommand):
    def __init__(self, collection: Collection,
                 kwargs):
        super().__init__("find", collection.name)
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.convert_to_camelcase(self.command_document)
        self.command_document = self.convert_to_camelcase(self.command_document)


class FindAndModifyCommand(BaseCommand):
    def __init__(self, collection: Collection,
                 kwargs):
        super().__init__("findAndModify", collection.name)
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = self.convert_to_camelcase(self.command_document)

class DeleteCommand(BaseCommand):
    def __init__(self, collection: Collection, filter,
                 limit, collation, kwargs):
        super().__init__("delete", collection.name)
        self.command_document = {"deletes": [SON({"q": filter, "limit": limit})]}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = self.convert_to_camelcase(self.command_document)


