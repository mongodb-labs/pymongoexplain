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


from pymongo import monitoring, MongoClient
from pymongo.collection import Collection, ReturnDocument
from pymongo.cursor import CursorType
from pymongo.common import BaseObject
from .explainable_collection import ExplainCollection
import sys
from bson.son import SON

old_update_one = Collection.update_one
old_replace_one = Collection.replace_one
old_update_many = Collection.update_many
old_delete_one = Collection.delete_one
old_delete_many = Collection.delete_many
old_aggregate = Collection.aggregate
old_watch = Collection.watch
old_find = Collection.find
old_find_one = Collection.find_one
old_find_one_and_delete = Collection.find_one_and_delete
old_find_one_and_replace = Collection.find_one_and_replace
old_find_one_and_update = Collection.find_one_and_update
old_count_documents = Collection.count_documents
old_estimated_document_count = Collection.estimated_document_count
old_distinct = Collection.distinct

old_functions = Collection.update_one
old_replace_one = Collection.replace_one,
old_update_many = Collection.update_many,
old_delete_one = Collection.delete_one,
old_delete_many = Collection.delete_many,
old_aggregate = Collection.aggregate,
old_watch = Collection.watch,
old_find = Collection.find,
old_find_one = Collection.find_one,
old_find_one_and_delete = Collection.find_one_and_delete,
old_find_one_and_replace = Collection.find_one_and_replace,
old_find_one_and_update = Collection.find_one_and_update,
old_count_documents = Collection.count_documents,
old_estimated_document_count = Collection.estimated_document_count,
old_distinct = Collection.distinct

def update_one(self: Collection, filter, update, upsert=False,
                   bypass_document_validation=False, collation=None,
                   array_filters=None, session=None):
    print(ExplainCollection(self).update_one(filter, update, upsert,
                                             bypass_document_validation,
                                             collation, array_filters, session))
    old_update_one(self, filter, update)

def replace_one(self: Collection, filter, replacement, upsert=False,
            bypass_document_validation=False, collation=None, session=None):
    print(ExplainCollection(self).replace_one(filter, replacement, upsert,
            bypass_document_validation, collation, session))
    old_replace_one(self, filter, replacement, upsert,
            bypass_document_validation, collation, session)

def update_many(self: Collection, filter, update, upsert=False, array_filters=None,
            bypass_document_validation=False, collation=None, session=None):
    print(ExplainCollection(self).update_many(filter, update, upsert, array_filters,
            bypass_document_validation, collation, session))
    old_update_many(self, filter, update, upsert, array_filters,
            bypass_document_validation, collation, session)

def delete_one(self: Collection, filter, collation=None, session=None):
    print(ExplainCollection(self).delete_one(filter, collation, session))
    old_delete_one(self, filter, collation, session)

def delete_many(self: Collection, filter, collation=None, session=None):
    print(ExplainCollection(self).delete_many(filter, collation, session))
    old_delete_many(filter, collation, session)

def aggregate(self: Collection, pipeline, session=None, **kwargs):
    print(ExplainCollection(self).aggregate(pipeline, session, kwargs))
    old_aggregate(self, pipeline, session, kwargs)

def watch(self: Collection, pipeline=None, full_document=None, resume_after=None,
      max_await_time_ms=None, batch_size=None, collation=None,
          start_at_operation_time=None, session=None, start_after=None):
    print(ExplainCollection(self).watch(pipeline, full_document, resume_after,
      max_await_time_ms, batch_size, collation,
          start_at_operation_time, session, start_after))
    old_watch(self, pipeline, full_document, resume_after,
      max_await_time_ms, batch_size, collation,
          start_at_operation_time, session, start_after)

def find(self: Collection, filter=None, projection=None, skip=0, limit=0, no_cursor_timeout=False,
     cursor_type=CursorType.NON_TAILABLE, sort=None,
     allow_partial_results=False, oplog_replay=False, modifiers=None,
     batch_size=0, manipulate=True, collation=None, hint=None,
     max_scan=None, max_time_ms=None, max=None, min=None, return_key=False,
     show_record_id=False, snapshot=False, comment=None, session=None):
    print(ExplainCollection(self).find(filter, projection, skip, limit,
                                       no_cursor_timeout,
     cursor_type, sort,
     allow_partial_results, oplog_replay, modifiers,
     batch_size, manipulate, collation, hint,
     max_scan, max_time_ms, max, min, return_key,
     show_record_id, snapshot, comment, session))
    old_find(self, filter, projection, skip, limit,
                                       no_cursor_timeout,
     cursor_type, sort,
     allow_partial_results, oplog_replay, modifiers,
     batch_size, manipulate, collation, hint,
     max_scan, max_time_ms, max, min, return_key,
     show_record_id, snapshot, comment, session)

def find_one(self: Collection, filter=None, *args, **kwargs):
    print(ExplainCollection(self).replace_one(filter, args, kwargs))
    old_find_one(self, filter, args, kwargs)

def find_one_and_delete(self: Collection, filter, projection=None, sort=None, session=None,
                     **kwargs):
    print(ExplainCollection(self).find_one_and_delete(filter, projection, sort, session,
                     **kwargs))
    old_find_one_and_delete(filter, projection, sort, session,
                     **kwargs)

def find_one_and_replace(self: Collection, filter, replacement, projection=None, sort=None,
                      return_document=ReturnDocument.BEFORE, session=None,
                         **kwargs):
    print(ExplainCollection(self).find_one_and_replace(filter, replacement, projection, sort,
                      return_document, session,
                         **kwargs))
    old_find_one_and_replace(filter, replacement, projection, sort,
                      return_document, session,
                         **kwargs)

def find_one_and_update(self: Collection, filter, update, projection=None, sort=None,
                     return_document=ReturnDocument.BEFORE,
                        array_filters=None, session=None, **kwargs):
    print(ExplainCollection(self).find_one_and_update(filter, update, projection, sort,
                     return_document,
                        array_filters, session, **kwargs))
    old_find_one_and_update(filter, update, projection, sort,
                     return_document,
                        array_filters, session, **kwargs)

def count_documents(self: Collection, filter, session=None, **kwargs):
    print(ExplainCollection(self).count_documents(filter, session, **kwargs))
    old_count_documents(filter, session, **kwargs)

def estimated_document_count(self: Collection, **kwargs):
    print(ExplainCollection(self).estimated_document_count(kwargs))
    old_estimated_document_count(self, kwargs)

def distinct(self: Collection, key, filter=None, session=None, **kwargs):
    print(ExplainCollection(self).distinct(key, filter, session, **kwargs))
    old_distinct(self, key, filter, session, **kwargs)

Collection.update_one =update_one
Collection.replace_one =replace_one
Collection.update_many =update_many
Collection.delete_many =delete_many
Collection.delete_one =delete_one
Collection.aggregate =aggregate
Collection.watch =watch
Collection.find =find
Collection.find_one =find_one
Collection.find_one_and_delete =find_one_and_delete
Collection.find_one_and_replace =find_one_and_replace
Collection.find_one_and_update =find_one_and_update
Collection.count_documents =count_documents
Collection.estimated_document_count =estimated_document_count
Collection.distinct =distinct

if __name__ == '__main__':
    for file in sys.argv[1:]:
        with open(file) as f:
            exec(f.read())