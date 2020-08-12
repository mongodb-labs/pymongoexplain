==============
PyMongoExplain
==============

:Info: Explain collections in PyMongo. See
       `GitHub <https://github.com/mongodb-labs/pymongoexplain>`_
       for the latest source.
:Author: Julius Park

About
=====
This package provides an ``ExplainableCollection`` class that allows PyMongo's Collection methods to be explained_

PyMongoExplain greatly simplifies the amount of effort needed to explain commands.
For example, suppose we wanted to explain the following ``update_one``::

    collection.update_one({"quantity": 1057, "category": "apparel"},{"$set": {"reorder": True}})


Before PyMongoExplain, one would need to convert the update_one into the equivalent MongoDB command::

    collection.database.command(SON([('explain', SON([('update', 'products'), ('updates', [{'q': {'quantity': 1057, 'category': 'apparel'}, 'upsert': False, 'multi': False, 'u': {'$set': {'reorder': True}}}])])), ('verbosity', 'queryPlanner')]))


After PyMongoExplain::

    ExplainableCollection(collection).update_one({"quantity": 1057, "category": "apparel"},{"$set": {"reorder": True}})

.. _explained: https://docs.mongodb.com/master/reference/command/explain/#dbcmd.explain.

Installation
============

To install this package simply use pip::

    pip install pymongoexplain

Support / Feedback
==================

For questions, discussions, or general technical support, visit the `MongoDB Community Forums <https://developer.mongodb.com/community/forums/tag/python>`_.
The MongoDB Community Forums are a centralized place to connect with other MongoDB users, ask questions, and get answers.

Bugs / Feature Requests
=======================

Think you’ve found a bug? Want to see a new feature in PyMongoExplain?
Please open an issue on this `GitHub repository <https://github.com/mongodb-labs/pymongoexplain>`_.

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

PyMongoExplain requires `PyMongo>=3.10,<4 <https://github.com/mongodb/mongo-python-driver/>`_

Testing
=======

The easiest way to run the tests is to run **python setup.py test** in
the root of the distribution.

Tutorial
========

PyMongo operations in existing application code can be explained by swapping ``Collection`` objects with ``ExplainableCollection``
objects. The ``ExplainableCollection`` class provides all CRUD API methods provided by PyMongo's ``Collection``,
but using this class to run operations runs explain on them, instead of executing them.

To run explain on a command, first instantiate an ``ExplainableCollection`` from the ``Collection`` object originally used to run the command::

    from pymongoexplain import ExplainableCollection

    collection = client.db.products
    explain = ExplainableCollection(collection)

Now you are ready to explain some commands. Remember that explaining a command does not execute it::

    result = explain.update_one({"quantity": 1057, "category": "apparel"}, {"$set": {"reorder": True}})

Now ``result`` will contain the output of running explain on the given ``update_one`` command::

    {'ok': 1.0,
     'operationTime': Timestamp(1595603051, 3),
     'queryPlanner': {'indexFilterSet': False,
                      'namespace': 'db.products',
                      'parsedQuery': {'$and': [{'category': {'$eq': 'apparel'}},
                                               {'quantity': {'$eq': 1057}}]},
                      'planCacheKey': 'CD8F6D8F',
                      'plannerVersion': 1,
                      'queryHash': 'CD8F6D8F',
                      'rejectedPlans': [],
                      'winningPlan': {'inputStage': {'direction': 'forward',
                                                     'filter': {'$and': [{'category': {'$eq': 'apparel'}},
                                                                         {'quantity': {'$eq': 1057}}]},
                                                     'stage': 'COLLSCAN'},
                                      'stage': 'UPDATE'}},
     'serverInfo': {'gitVersion': '27f5c1ee9f513f29fe30b8ebefed99581428c6e1',
                    'host': 'Juliuss-MBP.verizon.net',
                    'port': 27017,
                    'version': '4.4.0-rc13'}}


Since ``ExplainableCollection`` instances provide all the same methods provided by ``Collection`` instances, explaining operations in your application code is a simple matter of replacing ``Collection`` instances in your application code with ``ExplainableCollection`` instances.


Explaining commands in a script
-------------------------------

You can also run explain on all commands within a Python script using our CLI tool.
Given a script that contains ``pymongo`` commands within it, you can simply run::

    python3 -m pymongoexplain <path/to/your/script.py>

This will log the explain output for every single command
within the specified script, **in addition to running every command** in the script itself. Do note that because the
explain output is generated using the `logging <https://docs.python.org/3/library/logging.html>`_ module,
if your script configures logging module there are certain things to keep in mind:

- if your script sets the `logging level <https://docs.python.org/3/library/logging.html#logging-levels>`_ higher than INFO, the explain output will be suppressed entirely.
- the explain output will be sent to whatever stream your script configures the logging module to send output to.

Any positional parameters or arguments required by your script can be
simply be appended to the invocation as follows::

    python3 -m pymongoexplain <path/to/your/script.py> [PARAMS] [--optname OPTS]


Limitations
-----------

This package does not support the fluent `Cursor API <https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html>`_,
so if you attempt to use it like so::

    ExplainableCollection(collection).find({}).sort(...)

Instead pass all the arguments to the find() call, like so::

    ExplainableCollection(collection).find({}, sort=...)