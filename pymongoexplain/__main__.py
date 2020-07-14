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
import sys
from bson.son import SON

class CommandLogger(monitoring.CommandListener):
    def __init__(self):
        self.payloads = []

    def started(self, event):
        self.payloads.append(event.command)

    def succeeded(self, event):
        pass

    def failed(self, event):
        pass

if __name__ == '__main__':

    for file in sys.argv[1:]:
        with open(file) as f:
            logger = CommandLogger()
            monitoring.register(logger)
            l = ""
            for line in f.readlines():
                l = l+line
                try:
                    exec(l)
                    l = ""
                except:
                    continue
                collections = [i for i in locals().values() if type(i)
                              == Collection]
                for collection in collections:
                    for payload in logger.payloads:
                        payload = SON([("explain", payload), ("verbosity", "queryPlanner")])
                        print(collection.database.command(payload))
                        logger.payloads = []
