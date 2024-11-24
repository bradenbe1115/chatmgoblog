import abc
import pymongo
from ingest_mgoblog_data.common import models
from typing import Union

# Global variables for db and table names regardless of repository abstraction
LANDING_DATABASE_NAME = "landing"
PROCESSED_DATABASE_NAME = "processed"
MGOBLOG_CONTENT_COLLECTION_NAME = "mgoblog_content"


class AbstractMgoBlogContentRepository(abc.ABC):

    def add_raw_mgoblog_content(self, mgoblog_content_landing_data: list[models.MgoblogContentLandingDataSchema]):
        """
        Upserts raw Mgoblog content data into the repository

        Parameters:
            data (list[MgoblogContentLandingDataSchema]): list of Mgoblog raw data content

        """
        self._add_raw_mgoblog_content(mgoblog_content_landing_data=mgoblog_content_landing_data)

    @abc.abstractmethod
    def _add_raw_mgoblog_content(self, mgoblog_content_landing_data: list[models.MgoblogContentLandingDataSchema]):
        raise NotImplementedError
    
    def get_raw_mgoblog_content(self, url: str) -> Union[models.MgoblogContentLandingDataSchema, None]:
        """
            Retrieves raw Mgoblog content from database via matching url.

            Returns None if no matching content is found.

            Parameters:
                url (str): URL of content to be searched for in database.
        """
        return self._get_raw_mgoblog_content(url)
    
    @abc.abstractmethod
    def _get_raw_mgoblog_content(self, url: str) -> Union[models.MgoblogContentLandingDataSchema, None]:
        raise NotImplementedError
    
    def add_processed_mgoblog_content(self, mgoblog_processed_data: list[dict]):
        self._add_processed_mgoblog_content(mgoblog_processed_data=mgoblog_processed_data)

    @abc.abstractmethod
    def _add_processed_mgoblog_content(self, mgoblog_processed_data: list[dict]):
        raise NotImplementedError
    

class PyMongoMgoBlogContentRepository(AbstractMgoBlogContentRepository):

    def __init__(self, client: pymongo.MongoClient):
        self.client = client

    def _add_raw_mgoblog_content(self, mgoblog_content_landing_data):

        operations = [pymongo.UpdateOne({'url': x.url},  {"$set": x.__dict__}, upsert=True) for x in mgoblog_content_landing_data]


        result = self.client[LANDING_DATABASE_NAME][
            MGOBLOG_CONTENT_COLLECTION_NAME
        ].bulk_write(operations)
        print(result)

    def _get_raw_mgoblog_content(self, url) -> Union[models.MgoblogContentLandingDataSchema, None]:
        result_set = self.client[LANDING_DATABASE_NAME][MGOBLOG_CONTENT_COLLECTION_NAME].find_one({'url': url})
        if result_set:
            result = models.MgoblogContentLandingDataSchema(**result_set)
            return result
        
        return None
    
    def _add_processed_mgoblog_content(self, mgoblog_processed_data: list[models.MgoblogContentProcessedDataSchema]):
        
        operations = [pymongo.UpdateOne({'url': x.url},  {"$set": x.__dict__}, upsert=True) for x in mgoblog_processed_data]

        result = self.client[PROCESSED_DATABASE_NAME][
            MGOBLOG_CONTENT_COLLECTION_NAME
        ].bulk_write(operations)
        print(result)
    