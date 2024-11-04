import abc
import pymongo
from ingest_mgoblog_data.common.models import MgoblogContentLandingDataSchema
from typing import Union


class AbstractMgoBlogContentRepository(abc.ABC):

    def add_raw_mgoblog_content(self, data: list[MgoblogContentLandingDataSchema]):
        """
        Upserts raw Mgoblog content data into the repository

        Parameters:
            data (list[MgoblogContentLandingDataSchema]): list of Mgoblog raw data content

        """
        self._add_raw_mgoblog_content(data=data)

    @abc.abstractmethod
    def _add_raw_mgoblog_content(self, data: list[MgoblogContentLandingDataSchema]):
        raise NotImplementedError
    
    def get_raw_mgoblog_content(self, url: str) -> Union[dict, None]:
        """
            Retrieves raw Mgoblog content from database via matching url.

            Returns None if no matching content is found.

            Parameters:
                url (str): URL of content to be searched for in database.
        """
        return self._get_raw_mgoblog_content(url)
    
    @abc.abstractmethod
    def _get_raw_mgoblog_content(self, url: str) -> Union[dict, None]:
        raise NotImplementedError

class PyMongoMgoBlogContentRepository(AbstractMgoBlogContentRepository):

    def __init__(
        self, db_uri: str, database_name: str, raw_mgoblog_content_collection_name: str, port: int=27017
    ):
        self.db_uri = db_uri
        self.port = port
        self.database_name = database_name
        self.raw_mgoblog_content_collection_name = raw_mgoblog_content_collection_name

    @property
    def client(self):
        return pymongo.MongoClient(self.db_uri, self.port)

    def _add_raw_mgoblog_content(self, data):

        operations = [pymongo.UpdateOne({'url': x.url},  {"$set": x.__dict__}, upsert=True) for x in data]


        self.client[self.database_name][
            self.raw_mgoblog_content_collection_name
        ].bulk_write(operations)

    def _get_raw_mgoblog_content(self, url) -> Union[dict, None]:
        return self.client[self.database_name][self.raw_mgoblog_content_collection_name].find_one({'url': url})