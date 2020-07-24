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
from pymongo.helpers import _index_document, _fields_list_to_dict
from pymongo.collation import validate_collation_or_none
from .utils import convert_to_camelcase


Document = Union[dict, SON]


class BaseCommand():
    def __init__(self, collection, collation):
        self.command_document = {}
        collation = validate_collation_or_none(collation)
        if collation is not None:
            self.command_document["collation"] = collation
        self.collection = collection

    @property
    def command_name(self):
        """New command classes will specify the command name here."""
        return None

    def get_SON(self):
        cmd = SON([(self.command_name, self.collection)])
        cmd.update(self.command_document)
        return cmd


class UpdateCommand(BaseCommand):
    def __init__(self, collection: Collection, filter, update,
                 upsert=None, multi=None, collation=None, array_filters=None,
                 hint=None, ordered=None, write_concern=None,
                 bypass_document_validation=None, comment=None):
        super().__init__(collection.name, collation)
        update_doc = {"q": filter, "u": update}
        self.command_document["updates"] = [update_doc]
        if upsert is not None:
            self.command_document["updates"][0]["upsert"] = upsert

        if multi is not None:
            self.command_document["updates"][0]["multi"] = multi

        if array_filters is not None:
            self.command_document["updates"][0]["array_filters"] = array_filters

        if hint is not None:
            self.command_document["updates"][0]["hint"] = hint if \
                        isinstance(hint, str) else _index_document(hint)

        if ordered is not None:
            self.command_document["ordered"] = ordered

        if write_concern is not None:
            self.command_document["write_concern"] = write_concern

        if bypass_document_validation is not None and \
                bypass_document_validation is not False:
            self.command_document["bypass_document_validation"] = bypass_document_validation

        if comment is not None:
            self.command_document["comment"] = comment

        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "update"


class DistinctCommand(BaseCommand):
    def __init__(self, collection: Collection, key, filter,
                 kwargs):
        super().__init__(collection.name, kwargs.pop("collation", None))
        self.command_document.update({"key": key, "query": filter})

        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "distinct"


class AggregateCommand(BaseCommand):
    def __init__(self, collection: Collection, pipeline,
                 cursor_options,
                 kwargs):

        super().__init__(collection.name, kwargs.pop("collation", None))
        self.command_document.update({"pipeline": pipeline, "cursor":
            cursor_options})

        for key, value in kwargs.items():
            if key == "batchSize":
                if value == 0:
                    continue
                self.command_document["cursor"]["batchSize"] = value
            else:
                self.command_document[key] = value

        self.command_document = convert_to_camelcase(
            self.command_document)

    @property
    def command_name(self):
        return "aggregate"


class CountCommand(BaseCommand):
    def __init__(self, collection: Collection, filter, kwargs):
        super().__init__(collection.name, kwargs.pop("collation", None))
        self.command_document.update({"query": filter})
        for key, value in kwargs.items():
            self.command_document[key] = value
        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "count"


class FindCommand(BaseCommand):
    def __init__(self, collection: Collection,
                 kwargs):
        super().__init__(collection.name, kwargs.pop("collation", None))
        for key, value in kwargs.items():
            if key == "projection" and value is not None:
                self.command_document["projection"] = _fields_list_to_dict(
                    value, "projection")
            elif key == "sort":
                self.command_document["sort"] = _index_document(
                    value)
            else:
                self.command_document[key] = value

        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "find"


class FindAndModifyCommand(BaseCommand):
    def __init__(self, collection: Collection,
                 kwargs):
        super().__init__(collection.name, kwargs.pop("collation", None))
        for key, value in kwargs.items():
            if key == "update" and kwargs.get("replacement", None) is not None:
                continue
            if key == "hint":
                self.command_document["hint"] = value if \
                    isinstance(value, str) else _index_document(value)
            elif key == "replacement":
                self.command_document["update"] = value
            elif key == "sort" and value is not None:
                self.command_document["sort"] = _index_document(
                    value)
            else:
                self.command_document[key] = value
        self.command_document = convert_to_camelcase(self.command_document)

    @property
    def command_name(self):
        return "findAndModify"


class DeleteCommand(BaseCommand):
    def __init__(self, collection: Collection, filter,
                 limit, collation, kwargs):
        super().__init__(collection.name, kwargs.pop("collation", None))
        self.command_document["deletes"] = [{"q": filter, "limit":
            limit}]
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
