from asyncio import coroutine

import muffin
import peewee

import pytest
from peewee_async import _run_sql


@pytest.fixture(scope='session')
def app(loop):
    app = muffin.Application(
        'peewee', loop=loop,
        PLUGINS=['muffin_peewee_async'],
        PEEWEE_ASYNC_CONNECTION='postgres+aiopg://postgres:@localhost:5432/postgres',
    )
    yield app
    with app.ps.peewee_async.manager.allow_sync():
        app.ps.peewee_async.router.model.drop_table()


@pytest.fixture(scope='session')
def model(app):
    @app.ps.peewee_async.register
    class Test(peewee.Model):
        data = peewee.CharField()

    with app.ps.peewee_async.manager.allow_sync():
        Test.create_table()
    yield Test
    with app.ps.peewee_async.manager.allow_sync():
        Test.drop_table()


@pytest.fixture(autouse=True)
@coroutine
def transaction(app, request):
    """Clean changes after test."""
    trans = app.ps.peewee_async.database.transaction_async()

    yield from trans.db.push_transaction_async()
    if trans.db.transaction_depth_async() == 1:
        yield from _run_sql(trans.db, 'BEGIN')

    @coroutine
    def fin():
        yield from trans.__aexit__()
    request.addfinalizer(fin)

    return True
