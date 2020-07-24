This package provides an ``ExplainCollection`` class
that allows that allows PyMongo's Collection methods to be explained_

.. _explained: https://docs.mongodb.com/master/reference/command/explain/#dbcmd.explain.


Tutorial
########
The intended use case for this package is to allow ``pymongo`` commands to be easily explained_.
This can be done by simply swapping out ``Collection`` for ``ExplainCollection``,
which has the same methods but will run explain on them **instead** of executing them.
The first step is to create a ``MongoClient`` instance, then, you can simply get a collection instance, and then wrap it in the ``ExplainCollection`` class.::

    collection = client.db.products
    explain = ExplainCollection(collection)

Now you are ready to explain some commands. Remember that these commands will not be executed, they will simply have explain
run on them.::

    res = explain.update_one({"quantity": 1057, "category": "apparel"}, {"$set": {"reorder": True}})

The value of ``res`` will be whatever the output of explain for that ``update_one`` command is: ::

    {'$clusterTime':
        {'signature': {
            'keyId': 0, 'hash': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
            'clusterTime': Timestamp(1595603051, 3)},
            'serverInfo': {'host': 'Juliuss-MBP.verizon.net', 'version': '4.4.0-rc13', 'port': 27017, 'gitVersion': '27f5c1ee9f513f29fe30b8ebefed99581428c6e1'},
            'queryPlanner':
                {'plannerVersion': 1,
                'queryHash': 'CD8F6D8F',
                'parsedQuery':
                    {'$and': [
                    {'category': {'$eq': 'apparel'}},
                    {'quantity': {'$eq': 1057}}]},
                    'namespace': 'db.products',
                    'indexFilterSet': False,
                    'winningPlan':
                    {'inputStage':
                        {'filter':
                            {'$and': [
                                {'category': {'$eq': 'apparel'}},
                      {'quantity': {'$eq': 1057}}]},
                       'stage': 'COLLSCAN', 'direction': 'forward'},
                       'stage': 'UPDATE'}, 'planCacheKey': 'CD8F6D8F',
                      'rejectedPlans': []}, 'ok': 1.0,
                      'operationTime': Timestamp(1595603051, 3)}


This diagnostic information should hopefully help you understand what the problem is with your commands. Because
``ExplainCollection`` implements all the methods of ``Collection``, you can simply replace instances of collection with
an ``ExplainCollection`` to get this information.

CLI Tool
########

You can also run explain on all commands within a Python script using our CLI tool.
Given a script that contains ``pymongo`` commands within it, you can simply run: ::

    python3 -m pymongoexplain ../<pymongoscript>.py

This will print out the explain output for every single command
within that script, in addition to running the script itself.

If you have arguments that need to be supplied, you can simply append those
after the script path: ::

    python3 -m pymongoexplain ../<pymongoscript>.py <arg1> <arg2>