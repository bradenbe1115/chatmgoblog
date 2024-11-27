from __future__ import annotations
import abc
import chromadb

from index_content.common import vector_db

class AbstractUnitOfWork(abc.ABC):
    index: vector_db.AbstractVectorDB

    def __enter__(self) -> AbstractUnitOfWork:
        return self
    
    def __exist__(self, *args):
        pass

def chromadb_client_factory() -> chromadb.HttpClient:
    host = "http://vector_db:6333"
    port = 6333
    return chromadb.HttpClient(host=host, port=port)

class ChromaDBUnitOfWork(AbstractUnitOfWork):

    def __init__(self, client_factory=chromadb_client_factory):
        self.client_factory = client_factory

    def __enter__(self):
        self.client = self.client_factory()
        self.index = vector_db.ChromaVectorDB(self.client)
        return super().__enter__()