from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
from ingest_mgoblog_data.common.repository import PyMongoMgoBlogContentRepository 

DB_URI = "elt_db"
DB_NAME = "landing"
COLLECTION_NAME = "mgoblog_content"

def main():

    ws = MGoBlogWebScraper()
    start_url = "https://www.mgoblog.com/"

    results = ws.get_content(start_url=start_url, max_iteration=1)
    print(f"{len(results)} pages scraped starting at {start_url}")

    repo = PyMongoMgoBlogContentRepository(db_uri=DB_URI, database_name=DB_NAME, raw_mgoblog_content_collection_name=COLLECTION_NAME)

    repo.add_raw_mgoblog_content(results)

if __name__ == "__main__":
    main()