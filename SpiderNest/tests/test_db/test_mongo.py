"""
author: thomaszdxsn
"""
import pytest
import pytest_twisted
import pymongo
from dynaconf import settings as dyna_settings

from ...db.mongo import insert_item


@pytest.fixture
def db():
    client = pymongo.MongoClient(dyna_settings['MONGO_URI'])
    db_name = dyna_settings['MONGO_DB_NAME']
    print(db_name)
    yield client[db_name]
    client.drop_database(db_name)
    client.close()


@pytest_twisted.inlineCallbacks
def test_insert_item(db):
    yield insert_item('test-insert', {'1': 1})
    docs = db['test-insert'].find()
    assert docs.count() == 1
    doc = docs.next()
    del doc['_id']
    assert doc == {'1': 1}
