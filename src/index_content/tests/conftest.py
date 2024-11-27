import pytest
import chromadb

@pytest.fixture
def test_vector_db_client():
    host, port = "http://test_vector_db:6333", 6333
    client = chromadb.HttpClient(host, port)
    yield client
