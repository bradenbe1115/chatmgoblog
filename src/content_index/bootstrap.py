import chromadb
from content_index.common.index import ChromaDBIndex

def chromadb_client_factory() -> chromadb.HttpClient:
    host, port = "http://vector_db:6333", 6333
    return chromadb.HttpClient(host, port)

def bootstrap():
    index = ChromaDBIndex(client=chromadb_client_factory(), content_collection_name="mgoblog_content_embeddings")

    return {"index": index}