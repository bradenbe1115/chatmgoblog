from index_content.common import chunker
from common import vector_db, content_repository, models

import os

from index_content.common import embedder

DB_URI = "elt_db"
LANDING_DB_NAME = "landing"
PROCESSED_DB_NAME = "processed"
COLLECTION_NAME = "mgoblog_content"
HF_ACCESS_TOKEN = os.getenv("HUGGING_FACE_INFERENCE_API_ACCESS_TOKEN")
MODEL_ENDPOINT = "models/intfloat/multilingual-e5-large-instruct"

def index_mgoblog_content(urls: list[str]):

    repo = content_repository.PyMongoMgoBlogContentRepository(db_uri=DB_URI, landing_database_name=LANDING_DB_NAME, mgoblog_content_collection_name=COLLECTION_NAME, processed_database_name=PROCESSED_DB_NAME)

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