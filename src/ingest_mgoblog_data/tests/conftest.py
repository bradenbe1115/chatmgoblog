import pytest
import pymongo

@pytest.fixture
def test_elt_db_client():
    db_uri, port = "test_elt_db", 27017
    client = pymongo.MongoClient(db_uri, port)
    yield client
    client.close()
