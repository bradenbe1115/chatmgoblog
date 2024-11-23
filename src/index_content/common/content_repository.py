import abc
import pymongo
from typing import Union

from index_content.common import models

class AbstractMgoBlogContentRepository(abc.ABC):
    
    def get_processed_mgoblog_content(self, url: str) -> Union[models.MgoblogContentProcessedDataSchema, None]:
        """
            Retrieves raw Mgoblog content from database via matching url.

            Returns None if no matching content is found.

            Parameters:
                url (str): URL of content to be searched for in database.
        """
        return self._get_raw_mgoblog_content(url)
    
    @abc.abstractmethod
    def _get_processed_mgoblog_content(self, url: str) -> Union[models.MgoblogContentProcessedDataSchema, None]:
        raise NotImplementedError
    

class PyMongoMgoBlogContentRepository(AbstractMgoBlogContentRepository):

    def __init__(
        self, db_uri: str, mgoblog_content_collection_name: str,processed_database_name: str=None, port: int=27017
    ):
        self.db_uri = db_uri
        self.port = port
        self.processed_database_name = processed_database_name
        self.mgoblog_content_collection_name = mgoblog_content_collection_name

    @property
    def client(self):
        return pymongo.MongoClient(self.db_uri, self.port)

    def _get_processed_mgoblog_content(self, url) -> Union[models.MgoblogContentProcessedDataSchema, None]:
        result_set = self.client[self.processed_database_name][self.mgoblog_content_collection_name].find_one({'url': url})
        if result_set:
            result = models.MgoblogContentProcessedDataSchema(**result_set)
            return result
        
        return None
    