from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
from ingest_mgoblog_data.common import models
from ingest_mgoblog_data.common import repository

def scrape_mgoblog_data(web_scraper: MGoBlogWebScraper,repo: repository.AbstractMgoBlogContentRepository, start_url: str="https://www.mgoblog.com/additional-stories", iterations: int = 5, incremental=True):
    """
        Scrapes web pages from mgoblog to gather content

        Args:
            start_url (str): URL to start scraping from. Default is the additional content page on Mgoblog
            iterations (int): Number of pages to iterate through by hitting the next button on the blog
            incremental (bool): If True, will only scrape content from site and add to the db if url is not already in db. Otherwise, all content scraped will be added to the db and overwrite existing data.
    """

    stored_urls = []

    if incremental:
        print("Incremental strategy being used.")
        stored_urls = [x.url for x in repo.list_mgoblog_content()]

    results = web_scraper.get_content(start_url=start_url,max_iteration=iterations)
    print(f"{len(results)} pages scraped starting at {start_url}")

    results_to_add = [x for x in results if x.url not in stored_urls]
   
    
    if len(results_to_add) > 0: 
        print(f"{len(results_to_add)} results being added to db.")
        repo.add_raw_mgoblog_content(results_to_add)

    return {"landed_urls":[x.url for x in results_to_add]}

def process_mgoblog_data(repo: repository.AbstractMgoBlogContentRepository, event: dict):
    """
        Processes raw mgoblog content scraped from the website.

        Parses out repeatable, valuable metadata from web pages to store in repo.

        Args:
            event (dict): an event dictionary containing a key for "landed_urls" that points to a list of urls for raw mgoblog content
    """

    ws = MGoBlogWebScraper()
    results = []
    landed_urls = event["landed_urls"]

    raw_data = repo.get_raw_mgoblog_content(urls=landed_urls)
    
    for data in raw_data:
        processed_data = ws.extract_page_data(data.raw_html)
        full_data = models.MgoblogContentProcessedDataSchema(**{**processed_data, **data.__dict__})
        results.append(full_data)

    if len(results) > 0:
        repo.add_processed_mgoblog_content(results)
        return {"processed_urls":[x.url for x in results]}

    return {"processed_urls":[]}

def list_processed_mgoblog_content(repo: repository.AbstractMgoBlogContentRepository) -> list[models.MgoblogContentProcessedDataSchema]:
    """
        Lists all processed Mgoblog content stored in the repository
    """

    mgoblog_content = repo.list_mgoblog_content()

    if len(mgoblog_content) > 0:
        return mgoblog_content
    
    return []