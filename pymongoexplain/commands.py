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
from pymongo.helpers import _index_document
from .utils import convert_to_camelcase


Document = Union[dict, SON]


class BaseCommand():
    def __init__(self, collection):
        self.command_document = {}
        self.collection = collection

    @property
    def command_name(self):
        """New command classes will specify the command name here."""
        return None

    def get_SON(self):
        cmd = SON([(self.command_name, self.collection)])
        cmd.update(self.command_document)
        if self.command_document == {}:
            return {}
        return cmd


class UpdateCommand(BaseCommand):
    def __init__(self, collection: Collection, filter, update,
                 kwargs):
        super().__init__(collection.name)
        return_document = {
            "updates":[{"q": filter, "u": update}]
        }
        for key, value in kwargs.items():
            if key == "bypass_document_validation":
                return_document[key] = value
            elif key == "hint":
                if value is not {} and value is not None:
                    return_document["updates"][0]["hint"] = value if \
                        isinstance(value, str) else _index_document(value)
            else:
                return_document["updates"][0][key] = value
        self.command_document = convert_to_camelcase(return_document)

    @property
    def command_name(self):
        return "update"


class DistinctCommand(BaseCommand):
    def __init__(self, collection: Collection, key, filter, session,
                 kwargs):
        super().__init__(collection.name)
        self.command_document = {"key": key, "query": filter}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "distinct"


class AggregateCommand(BaseCommand):
    def __init__(self, collection: Collection, pipeline, session,
                 cursor_options,
                 kwargs, exclude_keys = []):
        super().__init__(collection.name)
        self.command_document = {"pipeline": pipeline, "cursor": cursor_options}
        for key, value in kwargs.items():
            if key == "batchSize":
                if value == 0:
                    continue
                self.command_document["cursor"]["batchSize"] = value
            else:
                self.command_document[key] = value

        self.command_document = convert_to_camelcase(
            self.command_document, exclude_keys=exclude_keys)

    @property
    def command_name(self):
        return "aggregate"

class CountCommand(BaseCommand):
    def __init__(self, collection: Collection, filter,
                 kwargs):
        super().__init__(collection.name)
        self.command_document = {"query": filter}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "count"


class FindCommand(BaseCommand):
    def __init__(self, collection: Collection,
                 kwargs):
        super().__init__(collection.name)
        if kwargs["filter"] == {}:
            self.command_document = {}
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "find"


class FindAndModifyCommand(BaseCommand):
    def __init__(self, collection: Collection,
                 kwargs):
        super().__init__(collection.name)
        for key, value in kwargs.items():
            if key == "update" and kwargs.get("replacement", None) is not None:
                continue
            if key == "hint":
                self.command_document["hint"] = value if \
                    isinstance(value, str) else _index_document(value)
            elif key == "replacement":
                self.command_document["update"] = value
            else:
                self.command_document[key] = value
        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "findAndModify"


class DeleteCommand(BaseCommand):
    def __init__(self, collection: Collection, filter,
                 limit, collation, kwargs):
        super().__init__(collection.name)
        self.command_document = {"deletes": [SON({"q": filter, "limit":
            limit, "collation": collation})]}
        for key, value in kwargs.items():
            if key == "hint":
                self.command_document["deletes"][0]["hint"] = value if \
                    isinstance(value, str) else _index_document(value)
            else:
                self.command_document[key] = value

        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "delete"
