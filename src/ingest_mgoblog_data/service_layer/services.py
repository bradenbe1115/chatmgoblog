from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
from ingest_mgoblog_data.common import models
from ingest_mgoblog_data.common import repository

def scrape_mgoblog_data(repo: repository.AbstractMgoBlogContentRepository, start_url: str="https://www.mgoblog.com/additional-stories", iterations: int = 5):
    """
        Scrapes web pages from mgoblog to gather content

        Args:
            start_url (str): URL to start scraping from. Default is the additional content page on Mgoblog
            iterations (int): Number of pages to iterate through by hitting the next button on the blog
    """

    ws = MGoBlogWebScraper()

    results = ws.get_content(start_url=start_url,max_iteration=iterations)
    print(f"{len(results)} pages scraped starting at {start_url}")

    repo.add_raw_mgoblog_content(results)

    return {"landed_urls":[x.url for x in results]}

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