from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
from ingest_mgoblog_data.common.repository import PyMongoMgoBlogContentRepository 

DB_URI = "elt_db"
LANDING_DB_NAME = "landing"
PROCESSED_DB_NAME = "processed"
COLLECTION_NAME = "mgoblog_content"

def scrape_mgoblog_data(iterations: int = 5):

    ws = MGoBlogWebScraper()
    start_url = "https://www.mgoblog.com/additional-stories"

    results = ws.get_content(start_url=start_url,max_iteration=iterations)
    print(f"{len(results)} pages scraped starting at {start_url}")

    repo = PyMongoMgoBlogContentRepository(db_uri=DB_URI, landing_database_name=LANDING_DB_NAME, mgoblog_content_collection_name=COLLECTION_NAME)

    repo.add_raw_mgoblog_content(results)

    return {"landed_urls":[x.url for x in results]}

def process_mgoblog_data(event: dict):

    ws = MGoBlogWebScraper()
    repo = PyMongoMgoBlogContentRepository(db_uri=DB_URI, landing_database_name=LANDING_DB_NAME, mgoblog_content_collection_name=COLLECTION_NAME, processed_database_name=PROCESSED_DB_NAME)

    results = []
    landed_urls = event["landed_urls"]
    for landed_url in landed_urls:

        raw_data = repo.get_raw_mgoblog_content(url=landed_url)
        processed_data = ws.extract_page_data(raw_data["raw_html"])
        full_data = {**processed_data, **raw_data}
        results.append(full_data)
    
    repo.add_processed_mgoblog_content(results)

    return