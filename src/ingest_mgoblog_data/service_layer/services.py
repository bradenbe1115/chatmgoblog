from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
from ingest_mgoblog_data.common import models
from ingest_mgoblog_data.service_layer import unit_of_work


def scrape_mgoblog_data(uow: unit_of_work.AbstractUnitOfWork, iterations: int = 5):

    ws = MGoBlogWebScraper()
    start_url = "https://www.mgoblog.com/additional-stories"

    results = ws.get_content(start_url=start_url,max_iteration=iterations)
    print(f"{len(results)} pages scraped starting at {start_url}")

    with uow:
        uow.content.add_raw_mgoblog_content(results)

    return {"landed_urls":[x.url for x in results]}

def process_mgoblog_data(uow: unit_of_work.AbstractUnitOfWork, event: dict):

    ws = MGoBlogWebScraper()
    results = []
    landed_urls = event["landed_urls"]

    with uow:
        raw_data = uow.content.get_raw_mgoblog_content(urls=landed_urls)
    
    for data in raw_data:
        processed_data = ws.extract_page_data(data.raw_html)
        full_data = models.MgoblogContentProcessedDataSchema(**{**processed_data, **data.__dict__})
        results.append(full_data)

    if len(results) > 0:
        with uow:
            uow.content.add_processed_mgoblog_content(results)
        return {"processed_urls":[x.url for x in results]}

    return {"process_urls":[]}