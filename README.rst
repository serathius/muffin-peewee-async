Muffin Peewee Async
#############

.. _description:

Muffin Peewee Async -- Peewee integration to Muffin framework using peewee-async.

Based on https://github.com/klen/muffin-peewee with an ability to execute asynchronous queries.


Installation
=============

**Muffin Peewee Async** should be installed using pip: ::

    pip install muffin-peewee-async


Usage
=====

Add `muffin_peewee_async` to `PLUGINS` in your Muffin Application configuration.

Or install it manually like this: ::

    db = muffin_peewee_async.Plugin(**{'options': 'here'})

    app = muffin.Application('test')
    app.install(db)


Options
-------

`PEEWEE_ASYNC_CONNECTION` -- connection string to your database (postgres://postgres:postgres@127.0.0.1)

`PEEWEE_ASYNC_CONNECTION_PARAMS` -- Additional params for connection ({})

`PEEWEE_ASYNC_MIGRATIONS_PATH` -- path to migration folder (migrations)

Queries
-------

::
    import peewee_async

    @app.ps.peewee_async.register
    class Test(peewee.Model):
        data = peewee.CharField()


    @app.register
    async def view(request):
        tests = await peewee_async.select(Test.select())
        return [t.data for t in tests]


Migrations
----------

Create migrations: ::

    $ muffin example:app pw_create [NAME] [--auto]


Run migrations: ::

    $ muffin example:app pw_migrate [NAME] [--fake]


Rollback migrations: ::

    $ muffin example:app pw_rollback NAME


Load/Dump data to CSV
---------------------

Dump table `test` to CSV file: ::

    $ muffin example:app pw_dump test


Load data from CSV file to table `test`: ::

    $ muffin example:app pw_load test


.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/serathius/muffin-peewee-async/issues

.. _contributing:

Contributing
============

Development of Muffin Peewee Async happens at: https://github.com/serathius/muffin-peewee-async


Contributors
=============

* serathius (Marek Siarkowicz)

.. _license:

License
=======

Licensed under a `MIT license`_.

.. _links:

.. _MIT license: http://opensource.org/licenses/MIT
