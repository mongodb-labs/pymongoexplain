==============
PyMongoExplain
==============

:Info: Explain collections in PyMongo. See
       `GitHub <https://github.com/mongodb-labs/pymongoexplain>`_
       for the latest source.
:Author: Julius Park

About
=====
This package provides an ``ExplainCollection`` class that allows PyMongo's Collection methods to be explained_

.. _explained: https://docs.mongodb.com/master/reference/command/explain/#dbcmd.explain.


Support / Feedback
==================

For questions, discussions, or general technical support, visit the MongoDB Community Forums.
The MongoDB Community Forums are a centralized place to connect with other MongoDB users, ask questions, and get answers.

Bugs / Feature Requests
=======================

Think you’ve found a bug? Want to see a new feature in PyMongoExplain?
Please open an issue on this GitHub repository.

How To Ask For Help
-------------------

Please include all of the following information when opening an issue:

- Detailed steps to reproduce the problem, including full traceback, if possible.
- The exact python version used, with patch level::

  $ python -c "import sys; print(sys.version)"

- The exact version of PyMongo used (if applicable), with patch level::

  $ python -c "import pymongo; print(pymongo.version); print(pymongo.has_c())"

- The exact version of PyMongoExplain used::

  $ python -c "import pymongoexplain; print(pymongoexplain.version)"


Dependencies
============

PyMongoExplain requires CPython 3.5+, and PyPy3.5+.

PyMongoExplain requires `PyMongo <https://github.com/mongodb/mongo-python-driver/>`_

Testing
=======

The easiest way to run the tests is to run **python setup.py test** in
the root of the distribution.

Tutorial
========

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
-------------------------------

You can also run explain on all commands within a Python script using our CLI tool.
Given a script that contains ``pymongo`` commands within it, you can simply run: ::

    python3 -m pymongoexplain <path/to/your/script.py>

This will print out the explain output for every single command
within that script, in addition to running the script itself.

Any positional parameters or arguments required by your script can be
simply be appended to the invocation as follows::

    python3 -m pymongoexplain <path/to/your/script.py> [PARAMS] [--optname OPTS]


