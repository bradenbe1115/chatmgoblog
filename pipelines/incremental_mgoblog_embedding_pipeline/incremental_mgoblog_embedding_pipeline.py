from ingest_mgoblog_data.service_layer import services as ingest_mgoblog_services
from ingest_mgoblog_data import bootstrap as ingest_mgoblog_bootstrap

from embed.service_layer.services import embed_content
from embed import bootstrap as embed_bootstrap

from content_index.service_layer import services as content_index_services
from content_index import bootstrap as content_index_bootstrap

import time

def find_content_not_embedded(processed_data, embedded_data):
    embedded_urls = [x.url for x in embedded_data]
    
    return [x for x in processed_data if x.url not in embedded_urls]

def incremental_mgoblog_embedding_pipeline():

    ingest_mgoblog_dependencies = ingest_mgoblog_bootstrap.bootstrap()

    mgoblog_content = ingest_mgoblog_services.list_processed_mgoblog_content(uow=ingest_mgoblog_dependencies["repo"])

    content_index_depencencies = content_index_bootstrap.bootstrap()
    embedded_content = content_index_services.list_mgoblog_content(uow=content_index_depencencies["repo"])

    content_to_embed = find_content_not_embedded(mgoblog_content, embedded_content)

    if len(content_to_embed) == 0:
        print("No content to embed. Exiting...")
        return 
    
    embed_dependencies = embed_bootstrap.RecursiveTextChunkerHuggingFaceMLE5Embedder()
    start_time = time.perf_counter()
    embedded_text = embed_content(chunker=embed_dependencies["chunker"], embedder=embed_dependencies["embedder"], text_data=[x.__dict__ for x in content_to_embed[0:25]], text_field_name="body")
    end_time = time.perf_counter()
    print(f"Embed Time: {end_time - start_time}")

    content_to_index = []
    for i in range(0,len(embedded_text)):
        item = embedded_text[i]
        if "embedded" in item.keys():
            url = item["url"]
            content_to_index.append({"id": f"{i}:{url}","url": url, "embedding": item['embedded'], "text": item['body']})

    content_index_services.add_mgoblog_content(uow=content_index_depencencies["uow"], data=content_to_index)


if __name__ == "__main__":
    incremental_mgoblog_embedding_pipeline()

