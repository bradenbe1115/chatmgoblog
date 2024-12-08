import pytest
import pymongo
import chromadb

@pytest.fixture
def test_elt_db_client():
    db_uri, port = "test_elt_db", 27017
    client = pymongo.MongoClient(db_uri, port)
    yield client
    client.close()

@pytest.fixture
def test_chromadb_client():
    host, port = "http://test_vector_db:6333", 6333
    client = chromadb.HttpClient(host, port)
    yield client
