from __future__ import annotations
import abc
from ingest_mgoblog_data import config
import pymongo

from ingest_mgoblog_data.common import repository

class AbstractUnitOfWork(abc.ABC):
    content = repository.AbstractMgoBlogContentRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        pass

def mongo_db_client_factory() -> pymongo.MongoClient:
    db_uri, port = config.get_mongo_db_info()
    return pymongo.MongoClient(db_uri, port)

class PymongoUnitOfWork(AbstractUnitOfWork):

    def __init__(self, client_factory=mongo_db_client_factory):
        self.client_factory = client_factory

    def __enter__(self):
        self.client = self.client_factory()
        self.content = repository.PyMongoMgoBlogContentRepository(self.client)
        return super().__enter__()
    
    def __exit__(self):
        self.client.close()
