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


from typing import Union, List, Dict

import pymongo
from pymongo.collection import Collection
from bson.son import SON

from .commands import AggregateCommand, FindCommand, CountCommand, \
    UpdateCommand, DistinctCommand, DeleteCommand, FindAndModifyCommand

Document = Union[dict, SON]


class ExplainableCollection():
    def __init__(self, collection, verbosity=None, comment=None):
        self.collection = collection
        self.last_cmd_payload = None
        self.verbosity = verbosity or "queryPlanner"
        self.comment = comment

    def _explain_command(self, command):
        command_son = command.get_SON()
        explain_command = SON([("explain", command_son)])
        explain_command["verbosity"] = self.verbosity
        if self.comment:
            explain_command["comment"] = self.comment
        self.last_cmd_payload = command_son
        return self.collection.database.command(explain_command)

    def update_one(self, filter, update, upsert=False,
                   bypass_document_validation=False,
                   collation=None, array_filters=None, hint=None,
                   session=None, **kwargs):
        command = UpdateCommand(self.collection, filter, update,
                                bypass_document_validation=
                                    bypass_document_validation,
                                array_filters=array_filters,
                                collation=collation, hint=hint,
                                upsert=upsert, multi=False)
        return self._explain_command(command)

    def update_many(self, filter: Document, update: Document, upsert=False,
                    array_filters=None, bypass_document_validation=False,
                    collation=None, hint=None, session=None, **kwargs):
        command = UpdateCommand(self.collection, filter, update, multi=True,
                                bypass_document_validation=bypass_document_validation, upsert=upsert, collation=collation, array_filters=array_filters, hint=hint)
        return self._explain_command(command)

    def distinct(self, key: str, filter: Document=None, session=None, **kwargs):
        command = DistinctCommand(self.collection, key, filter, kwargs)
        return self._explain_command(command)

    def aggregate(self, pipeline: List[Document], session=None, **kwargs):
        command = AggregateCommand(self.collection, pipeline,
                                   {}, kwargs)
        return self._explain_command(command)

    def estimated_document_count(self,
                                 **kwargs):

        command = CountCommand(self.collection, None, kwargs)
        return self._explain_command(command)

    def count_documents(self, filter: Document, session=None,
                                 **kwargs):

        command = AggregateCommand(self.collection, [{'$match': filter},
                                                     {'$group': {'n': {'$sum': 1}, '_id': 1}}]
                                   , {}, kwargs)
        return self._explain_command(command)

    def delete_one(self, filter: Document, collation=None, session=None,
                   **kwargs):
        limit = 1
        command = DeleteCommand(self.collection, filter, limit, collation,
                                kwargs)
        return self._explain_command(command)

    def delete_many(self, filter: Document, collation=None,
                    session=None, **kwargs: Dict[str, Union[int, str,
                                                            Document,
                                                      bool]]):
        limit = 0
        command = DeleteCommand(self.collection, filter, limit, collation,
                                kwargs)
        return self._explain_command(command)

    def watch(self, pipeline: Document = None, full_document: Document = None,
              resume_after= None,
              max_await_time_ms: int = None, batch_size: int = None,
              collation=None, start_at_operation_time=None, session=None,
              start_after=None):

        change_stream_options = {}
        if start_after:
            change_stream_options["startAfter"] = start_after
        if resume_after:
            change_stream_options["resumeAfter"] = resume_after
        if start_at_operation_time:
            change_stream_options["startAtOperationTime"] = start_at_operation_time
        if full_document:
            change_stream_options["fullDocument"] = full_document

        if pipeline is not None:
            pipeline = [{"$changeStream": change_stream_options}]+pipeline
        else:
            pipeline = [{"$changeStream": change_stream_options}]
        cursor_args = {}
        if batch_size:
            cursor_args["batchSize"] = batch_size
        command = AggregateCommand(self.collection, pipeline,
                                   cursor_args,
                                   {"collation":collation, "max_await_time_ms":
                                       max_await_time_ms})
        return self._explain_command(command)

    def find(self, filter: Document = None,
             **kwargs: Dict[str, Union[int, str,Document, bool]]):
        kwargs.update(locals())
        del kwargs["self"], kwargs["kwargs"]
        command = FindCommand(self.collection,
                              kwargs)

        return self._explain_command(command)

    def find_one(self, filter: Document = None, **kwargs: Dict[str,
                                                               Union[int, str,
                                                                Document, bool]]):
        kwargs.update(locals())
        del kwargs["self"], kwargs["kwargs"]
        kwargs["limit"] = 1
        command = FindCommand(self.collection, kwargs)
        return self._explain_command(command)

    def find_one_and_delete(self, filter: Document, projection: list = None,
                            sort: Document=None, session=None,
                        **kwargs):
        kwargs["query"] = filter
        kwargs["fields"] = projection
        kwargs["sort"] = sort
        kwargs["remove"] = True
        kwargs["session"] = session

        command = FindAndModifyCommand(self.collection,
                                       kwargs)
        return self._explain_command(command)

    def find_one_and_replace(self, filter: Document, replacement:
    Document={},
                            projection: list = None, sort=None,
                             return_document=pymongo.ReturnDocument.BEFORE,
                             session=None, **kwargs):
        kwargs["query"] = filter
        kwargs["fields"] = projection
        kwargs["sort"] = sort
        kwargs["new"] = False
        kwargs["update"] = replacement
        kwargs["session"] = session
        command = FindAndModifyCommand(self.collection,
                                       kwargs)
        return self._explain_command(command)

    def find_one_and_update(self, filter: Document, update: Document,
                            projection: list = None, sort=None,
                             return_document=pymongo.ReturnDocument.BEFORE,
                             session=None, **kwargs):
        kwargs["query"] = filter
        kwargs["fields"] = projection
        kwargs["sort"] = sort
        kwargs["upsert"] = False
        kwargs["update"] = update
        kwargs["session"] = session

        command = FindAndModifyCommand(self.collection,
                                       kwargs)
        return self._explain_command(command)

    def replace_one(self, filter: Document, replacement: Document,
                    upsert=False, bypass_document_validation=False,
                    collation=None, hint=None, session=None, **kwargs):
        command = UpdateCommand(self.collection, filter, update=replacement,
                                bypass_document_validation=bypass_document_validation,
                                hint=hint, collation=collation, multi=False, upsert=upsert)

        return self._explain_command(command)


# Alias
ExplainCollection = ExplainableCollection
