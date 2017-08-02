import asyncio


@asyncio.coroutine
def test_peewee(app, model):
    assert app.ps.peewee
    ins = yield from app.ps.peewee.manager.create(model, data='some')

    assert ins.id == 1
    assert ins.data == 'some'

    ins.data = 'other'
    yield from app.ps.peewee.manager.update(ins)

    test = yield from app.ps.peewee.manager.get(model)
    assert test.data == 'other'


def test_migrations(app, tmpdir):
    assert app.ps.peewee_async.router

    router = app.ps.peewee_async.router
    router.migrate_dir = str(tmpdir.mkdir('migrations'))

    with app.ps.peewee_async.manager.allow_sync():
        assert not router.todo
        assert not router.done
        assert not router.diff

    # Create migration
    name = app.manage.handlers['pw_create']('test')
    assert '001_test' == name
    with app.ps.peewee_async.manager.allow_sync():
        assert router.todo
        assert not router.done
        assert router.diff

    # Run migrations
    app.manage.handlers['pw_migrate']('test')
    with app.ps.peewee_async.manager.allow_sync():
        assert router.done
        assert not router.diff

    name = app.manage.handlers['pw_create']()
    assert '002_auto' == name


@asyncio.coroutine
def test_async_peewee(app):
    yield from app.ps.peewee.database.connect_async()
    assert app.ps.peewee.database.cursor_async()
    yield from app.ps.peewee.database.close_async()

    assert app.ps.peewee.database.obj.execution_context_depth() == 0
