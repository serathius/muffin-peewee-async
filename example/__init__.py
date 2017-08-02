import datetime

import random
import string
from asyncio import coroutine

from peewee_async import select, delete

import muffin

import peewee


app = muffin.Application(
    'example',

    PLUGINS=(
        'muffin_peewee_async',
    ),
    PEEWEE_ASYNC_CONNECTION='postgres+aiopg://postgres:postgres@localhost:5432/postgres',
    PEEWEE_ASYNC_MIGRATIONS_PATH='example/migrations',
)


@app.ps.peewee_async.register
class DataItem(peewee.Model):
    created = peewee.DateTimeField(default=datetime.datetime.utcnow)
    content = peewee.CharField()


@app.register('/')
@coroutine
def list(request):
    objects = yield from select(DataItem.select())
    template = """
        <html>
            <h3>Items: </h3>
            <a href="/generate"> Generate new Item </a>&nbsp;&nbsp;&nbsp;
            <a href="/clean"> Clean everything </a>
            <ul>%s</ul>
        </html>
    """ % "".join("<li>%s&nbsp;|&nbsp;%s</li>" % (d.created, d.content) for d in objects)
    return template


@app.register('/generate')
@coroutine
def generate(request):
    content = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    yield from app.ps.peewee_async.manager.create(DataItem, content=content)
    return muffin.HTTPFound('/')


@app.register('/clean')
@coroutine
def clean(request):
    yield from delete(DataItem.delete())
    return muffin.HTTPFound('/')
