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


from pymongo.collection import Collection
from .explainable_collection import ExplainCollection

import sys


old_function_names = ["update_one", "replace_one", "update_many", "delete_one",
                      "delete_many", "aggregate", "watch", "find", "find_one",
                      "find_one_and_delete", "find_one_and_replace",
                      "find_one_and_update", "count_documents",
                      "estimated_document_count", "distinct"]
old_functions = [getattr(Collection, i) for i in old_function_names]


def make_func(old_func, old_func_name):
    def new_func(self: Collection, *args, **kwargs):
        print(getattr(ExplainCollection(self), old_func_name)(*args,
                                                              **kwargs))
        return old_func(self, *args, **kwargs)
    return new_func


for old_func, old_func_name in zip(old_functions, old_function_names):
    setattr(Collection, old_func_name, make_func(old_func,
                                                 old_func_name))

if __name__ == '__main__':
    for file in sys.argv[1:]:
        with open(file) as f:
            exec(f.read())