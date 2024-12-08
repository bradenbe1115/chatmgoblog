from ingest_mgoblog_data.service_layer import services as ingest_mgoblog_services
from ingest_mgoblog_data import bootstrap as ingest_mgoblog_bootstrap

from embed.service_layer.services import embed
from embed import bootstrap as embed_bootstrap

from content_index.service_layer import services as content_index_services
from content_index import bootstrap as content_index_bootstrap

def mgoblog_ingestion_pipeline():

    
    ingest_mgoblog_dependencies = ingest_mgoblog_bootstrap.bootstrap()

    """
    scrape_output = ingest_mgoblog_services.scrape_mgoblog_data(uow=ingest_mgoblog_dependencies["uow"], iterations=10)

    ingest_mgoblog_services.process_mgoblog_data(uow=ingest_mgoblog_dependencies["uow"], event=scrape_output)
    """

    mgoblog_content = ingest_mgoblog_services.list_processed_mgoblog_content(uow=ingest_mgoblog_dependencies["uow"])

    embed_dependencies = embed_bootstrap.RecursiveTextChunkerHuggingFaceMLE5Embedder()
    embedded_text = embed(chunker=embed_dependencies["chunker"], embedder=embed_dependencies["embedder"], text_data=[x.body for x in mgoblog_content])

    content_index_depencencies = content_index_bootstrap.bootstrap()
    content_to_index = []
    for i in range(0,len(embedded_text)):
        item = embedded_text[i]
        url = mgoblog_content[item.index].url
        print(url)
        content_to_index.append({"id": f"{i}:{url}","url": url, "embedding": item.embedded_text, "text": item.text})

    print(len(content_to_index))
    content_index_services.add_mgoblog_content(uow=content_index_depencencies["uow"], data=content_to_index)

if __name__ == "__main__":
    mgoblog_ingestion_pipeline()

    
