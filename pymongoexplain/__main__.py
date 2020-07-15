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
from pymongo.collection import Collection
from pymongo.common import BaseObject
import sys
from bson.son import SON

old_update_one = Collection.update_one

def update_one(self: Collection, filter, update, upsert=False,
                   bypass_document_validation=False, collation=None,
                   array_filters=None, session=None):
        ret = old_update_one(self, filter, update)
        print(ret)
Collection.update_one = update_one

if __name__ == '__main__':
    for file in sys.argv[1:]:
        with open(file) as f:
            exec(f.read())