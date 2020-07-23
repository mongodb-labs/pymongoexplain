This package provides an ExplainCollection class
that allows common MongoDB commands to be explained

Tutorial
########
The intended use case for this package is to debug ``pymongo`` commands.
This can be done by simply swapping out ``Collection`` for ``ExplainCollection``,
which has the same functions but will run explain on them *instead* of executing them.
The first step is to create a ``MongoClient`` instance::

    client = MongoClient(serverSelectionTimeoutMS=1000, event_listeners=[logger])

Once this is done, you can simply get a collection instance, and then wrap it in the ``ExplainCollection`` class.::

    collection = client.db.products
    explain = ExplainCollection(collection)

Now you are ready to run some commands. Remember that these commands will not be executed, they will simply have explain
run on them.::

    res = explain.update_one({"quantity": 1057, "category": "apparel"}, {"$set": {"reorder": True}})

The value of ``res`` will be whatever the output of explain for that ``update_one`` command is: ::

    {
        'operationTime': Timestamp(1594666552, 1),
        'serverInfo': {
            'version': '4.4.0-rc10',
            'port': 27017,
            'gitVersion': '5218ee3e883b0230e121ae13a7640e0bc4a313ae',
            'host': 'Juliuss-MBP.verizon.net'
        },
        'ok': 1.0,
        '$clusterTime':{
                'signature': {'keyId': 0,
                'hash': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
                'clusterTime': Timestamp(1594666552, 1)
         },
        'queryPlanner': {
            'plannerVersion': 1,
            'rejectedPlans': [],
            'indexFilterSet': False,
            'namespace': 'db.products', 'winningPlan': {'stage': 'EOF'}
        }
    }

This diagnostic information should hopefully help you understand what the problem is with your commands. Because
``ExplainCollection`` implements all the methods of ``Collection``, you can simply replace instances of collection with
an ``ExplainCollection`` to get this information.