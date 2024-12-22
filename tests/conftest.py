import pytest
import time
import pymongo
import chromadb
from pathlib import Path
import requests
from user_query import config as user_query_config
from tenacity import retry, stop_after_delay

pytest.register_assert_rewrite("tests.e2e.api_client")

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

@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(user_query_config.get_api_url())

@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../../pipelines/user_query.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()