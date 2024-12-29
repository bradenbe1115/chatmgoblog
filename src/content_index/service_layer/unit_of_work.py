from __future__ import annotations
import abc
import chromadb

from content_index.common import index_repository

class AbstractUnitOfWork(abc.ABC):
    index: index_repository.AbstractIndexRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self
    
    def __exit__(self, *args):
        pass

def chromadb_client_factory() -> chromadb.HttpClient:
    host, port = "http://vector_db:6333", 6333
    return chromadb.HttpClient(host, port)

class ChromaDBUnitOfWork(AbstractUnitOfWork):

    def __init__(self, client_factory=chromadb_client_factory, content_collection_name:str="mgoblog_content_embeddings"):
        self.client_factory = client_factory
        self.content_collection_name = content_collection_name

    def __enter__(self):
        self.client = self.client_factory()
        self.index = index_repository.ChromaDBIndexRepository(self.client, content_collection_name=self.content_collection_name)
        return super().__enter__()