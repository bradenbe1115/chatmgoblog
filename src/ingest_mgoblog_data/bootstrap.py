from ingest_mgoblog_data import config
from ingest_mgoblog_data.common.repository import PyMongoMgoBlogContentRepository
from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
import pymongo

def mongo_db_client_factory() -> pymongo.MongoClient:
    db_uri, port = config.get_mongo_db_info()
    return pymongo.MongoClient(db_uri, port)

def bootstrap():

    return {"repo": PyMongoMgoBlogContentRepository(client=mongo_db_client_factory()), "web_scraper": MGoBlogWebScraper()}