from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper
from ingest_mgoblog_data.common import models
from ingest_mgoblog_data.common.repository import PyMongoMgoBlogContentRepository 
from embed_data.common import embedder, vector_db, chunker
import os

DB_URI = "elt_db"
LANDING_DB_NAME = "landing"
PROCESSED_DB_NAME = "processed"
COLLECTION_NAME = "mgoblog_content"
HF_ACCESS_TOKEN = os.getenv("HUGGING_FACE_INFERENCE_API_ACCESS_TOKEN")
MODEL_ENDPOINT = "models/intfloat/multilingual-e5-large-instruct"

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

        if raw_data is not None:
            processed_data = ws.extract_page_data(raw_data.raw_html)
            full_data = models.MgoblogContentProcessedDataSchema(**{**processed_data, **raw_data})
            results.append(full_data)

    if len(results) > 0:
        repo.add_processed_mgoblog_content(results)
        return {"processed_urls":[x.url for x in results]}

    return {"process_urls":[]}

def embed_mgoblog_data(urls: list[str]):

    repo = PyMongoMgoBlogContentRepository(db_uri=DB_URI, landing_database_name=LANDING_DB_NAME, mgoblog_content_collection_name=COLLECTION_NAME, processed_database_name=PROCESSED_DB_NAME)

    # Need to update to get a list of processed content
    processed_data = repo.get_processed_mgoblog_content(urls=urls)

    chunked_data = [
    {"url": d.url, "id": f"{d.url}:{i}", "text": text}
    for d in processed_data
    for i, text in enumerate(chunker.chunk_text(d.body))
    ]

    em = embedder.HuggingFaceInferenceAPIEmbedder(api_inputs=embedder.HuggingFaceInferenceAPIInputs(access_token=HF_ACCESS_TOKEN), model_endpoint=MODEL_ENDPOINT)
    embedded_text = em.embed_data(data=[x["text"] for x in chunked_data])

    embedded_data = []

    for i in range(0,len(embedded_text)):
        chunked_data[i]["embedding"] = embedded_text[i]
        embedded_data.append(models.MgoBlogContentEmbedding(**chunked_data))

    vd = vector_db.ChromaVectorDB()

    vd.insert_embedded_mgoblog_content(embeddings=embedded_data)
    return