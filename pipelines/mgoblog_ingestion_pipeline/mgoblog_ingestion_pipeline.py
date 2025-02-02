import argparse

from ingest_mgoblog_data.service_layer import services as ingest_mgoblog_services
from ingest_mgoblog_data import bootstrap as ingest_mgoblog_bootstrap

from embed.service_layer.services import embed_content
from embed import bootstrap as embed_bootstrap

from content_index.service_layer import services as content_index_services
from content_index import bootstrap as content_index_bootstrap

INGEST_MGOBLOG_BOOTSTRAP = ingest_mgoblog_bootstrap.bootstrap()
EMBED_BOOTSTRAP = embed_bootstrap.RecursiveTextChunkerHuggingFaceMLE5Embedder()
CONTENT_INDEX_BOOTSTRAP = content_index_bootstrap.bootstrap()

def find_content_not_embedded(processed_data, embedded_data):
    embedded_urls = [x.url for x in embedded_data]
    
    return [x for x in processed_data if x.url not in embedded_urls]

def mgoblog_ingestion_pipeline(iterations=1):

    print(f"Scraping content from Mgoblog. Number of iterations {iterations}")
    scrape_output = ingest_mgoblog_services.scrape_mgoblog_data(web_scraper=INGEST_MGOBLOG_BOOTSTRAP["web_scraper"],repo=INGEST_MGOBLOG_BOOTSTRAP["repo"], iterations=iterations, start_url="https://mgoblog.com/")
    print(f"Scraped {len(scrape_output['landed_urls'])} pages from MgoBlog.")

    print("Processing pages.")
    ingest_mgoblog_services.process_mgoblog_data(repo=INGEST_MGOBLOG_BOOTSTRAP["repo"], event=scrape_output)

    print("Looking for content that needs to be embedded.")
    mgoblog_content = ingest_mgoblog_services.list_processed_mgoblog_content(repo=INGEST_MGOBLOG_BOOTSTRAP["repo"])
    embedded_content = content_index_services.list_mgoblog_content(index=CONTENT_INDEX_BOOTSTRAP["index"])
    content_to_embed = find_content_not_embedded(mgoblog_content, embedded_content)
    print(f"{len(content_to_embed)} pages of content to embed.")

    if len(content_to_embed) > 0:
        embedded_text = embed_content(chunker=EMBED_BOOTSTRAP["chunker"], embedder=EMBED_BOOTSTRAP["embedder"], text_data=[x.__dict__ for x in content_to_embed], text_field_name="body")

        # Formatting data into expected content index schema
        content_to_index = []
        for i in range(0,len(embedded_text)):
            item = embedded_text[i]
            url = item["url"]
            content_to_index.append({"id": f"{i}:{url}","url": url, "embedding": item['embedded'], "text": item['body']})

        print(f"Uploading {len(content_to_index)} indexes into content index.")
        content_index_services.add_mgoblog_content(index=CONTENT_INDEX_BOOTSTRAP["index"], data=content_to_index)
    
    print("No new content to embed. Exiting..")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Mgoblog ingestion pipeline.")
    parser.add_argument("--iterations", type=int, default=1, help="Number of iterations for scraping content")
    
    args = parser.parse_args()
    mgoblog_ingestion_pipeline(iterations=args.iterations)

    
