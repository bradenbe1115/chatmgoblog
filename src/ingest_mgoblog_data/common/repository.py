import abc
import pymongo
from ingest_mgoblog_data.common import models

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
    
    def get_raw_mgoblog_content(self, urls: list[str]) -> list[models.MgoblogContentLandingDataSchema]:
        """
            Retrieves raw Mgoblog content from database via matching urls.

            Returns empty list if not matching content is found.

            Parameters:
                urls (list[str]): List of URLs of content to be searched for in database.
        """
        return self._get_raw_mgoblog_content(urls)
    
    @abc.abstractmethod
    def _get_raw_mgoblog_content(self, urls: list[str]) -> list[models.MgoblogContentLandingDataSchema]:
        raise NotImplementedError
    
    def add_processed_mgoblog_content(self, mgoblog_processed_data: list[dict]):
        self._add_processed_mgoblog_content(mgoblog_processed_data=mgoblog_processed_data)

    @abc.abstractmethod
    def _add_processed_mgoblog_content(self, mgoblog_processed_data: list[dict]):
        raise NotImplementedError
    
    def list_mgoblog_content(self) -> list[models.MgoblogContentProcessedDataSchema]:
        """
            Retrieves all processed mgoblog data from repo and returns it in a list
        """
        return self._list_mgoblog_content()
    
    @abc.abstractmethod
    def _list_mgoblog_content(self) -> list[models.MgoblogContentProcessedDataSchema]:
        raise NotImplementedError
    

class PyMongoMgoBlogContentRepository(AbstractMgoBlogContentRepository):

    def __init__(self, client: pymongo.MongoClient, landing_database_name: str = LANDING_DATABASE_NAME, mgoblog_content_collection_name: str = MGOBLOG_CONTENT_COLLECTION_NAME, processed_database_name: str = PROCESSED_DATABASE_NAME):
        self.client = client
        self.landing_database_name = landing_database_name
        self.processed_database_name = processed_database_name
        self.mgoblog_content_collection_name = mgoblog_content_collection_name

    def _add_raw_mgoblog_content(self, mgoblog_content_landing_data):

        operations = [pymongo.UpdateOne({'url': x.url},  {"$set": x.__dict__}, upsert=True) for x in mgoblog_content_landing_data]


        result = self.client[self.landing_database_name][
            self.mgoblog_content_collection_name
        ].bulk_write(operations)
        print(result)

    def _get_raw_mgoblog_content(self, urls: list[str]) -> list[models.MgoblogContentLandingDataSchema]:
        result_set = self.client[self.landing_database_name][self.mgoblog_content_collection_name].find({'url': {'$in': urls}})
        
        final_results = []
        if result_set:
            
            result_list = list(result_set)
            for result in result_list:
                final_results.append(models.MgoblogContentLandingDataSchema(**result))
        
        return final_results
    
    def _add_processed_mgoblog_content(self, mgoblog_processed_data: list[models.MgoblogContentProcessedDataSchema]):
        
        operations = [pymongo.UpdateOne({'url': x.url},  {"$set": x.__dict__}, upsert=True) for x in mgoblog_processed_data]

        result = self.client[self.processed_database_name][
            self.mgoblog_content_collection_name
        ].bulk_write(operations)
        print(result)

    def _list_mgoblog_content(self) -> list[models.MgoblogContentProcessedDataSchema]:

        result_set = self.client[self.processed_database_name][self.mgoblog_content_collection_name].find()

        final_result = []
        if result_set:

            for result in result_set:
                final_result.append(models.MgoblogContentProcessedDataSchema(**result))

        return final_result
    