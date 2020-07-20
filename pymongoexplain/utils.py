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


"""Utility functions"""


def convert_to_camelcase(d, exclude_keys=[]):
    if not isinstance(d, dict):
        return d
    ret = dict()
    for key in d.keys():
        if d[key] is None:
            continue
        if key in exclude_keys:
            ret[key] = d[key]
            continue
        new_key = key
        if "_" in key and key[0] != "_":
            new_key = key.split("_")[0] + ''.join(
                [i.capitalize() for i in key.split("_")[1:]])
        if isinstance(d[key], list):
            ret[new_key] = [convert_to_camelcase(
                i, exclude_keys=exclude_keys) for i in d[key]]
        elif isinstance(d[key], dict):
            ret[new_key] = convert_to_camelcase(d[key],
                                                     exclude_keys=exclude_keys)
        else:
            ret[new_key] = d[key]
    return ret
