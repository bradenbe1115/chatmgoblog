import pytest
import pymongo
import chromadb
import os
from langchain_openai import ChatOpenAI

pytest.register_assert_rewrite("tests.e2e.api_client")

@pytest.fixture
def test_elt_db_client():
    db_uri, port = "elt_db", 27017
    client = pymongo.MongoClient(db_uri, port)
    yield client
    client.close()

@pytest.fixture
def test_chromadb_client():
    host, port = "http://vector_db:6333", 6333
    client = chromadb.HttpClient(host, port)
    yield client

@pytest.fixture
def langchain_model():
    model = ChatOpenAI(model="gpt-4o-mini")
    yield model


