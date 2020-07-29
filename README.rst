This package provides an ``ExplainCollection`` class
that allows that allows PyMongo's Collection methods to be explained_

.. _explained: https://docs.mongodb.com/master/reference/command/explain/#dbcmd.explain.


Tutorial
########

PyMongo operations in existing application code can be explained by swapping ``Collection`` objects with ``ExplainCollection``
objects. The ``ExplainCollection`` class provides all CRUD API methods provided by PyMongo's ``Collection``,
but using this class to run operations runs explain on them, instead of executing them.

To run explain on a command, first instantiate an ``ExplainCollection`` from the ``Collection`` object originally used to run the command::

    collection = client.db.products
    explain = ExplainCollection(collection)

Now you are ready to explain some commands. Remember that explaining a command does not execute it::

    result = explain.update_one({"quantity": 1057, "category": "apparel"}, {"$set": {"reorder": True}})

Now ``result`` will contain the output of running explain on the given ``update_one`` command::

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


Since ``ExplainCollection`` instances provide all the same methods provided by ``Collection`` instances, explaining operations in your application code is a simple matter of replacing ``Collection`` instances in your application code with ``ExplainCollection`` instances.


Explaining commands in a script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also run explain on all commands within a Python script using our CLI tool.
Given a script that contains ``pymongo`` commands within it, you can simply run: ::

    python3 -m pymongoexplain <path/to/your/script.py>

This will log the explain output for every single command
within that script, in addition to running the script itself. Do note that because the logging of explain output is done
using the ``logging`` package, if you configure logging in your script to any level above ``logging.INFO``, the output
will be suppressed. Additionally, if you redirect logging output to a file it will also be suppressed and will write to that file.

Any positional parameters or arguments required by your script can be
simply be appended to the invocation as follows::

    python3 -m pymongoexplain <path/to/your/script.py> [PARAMS] [--optname OPTS]