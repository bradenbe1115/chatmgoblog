from embed.service_layer.services import embed
from embed import bootstrap as embed_bootstrap

from content_index.service_layer import services as content_index_services
from content_index import bootstrap as content_index_bootstrap


def user_query(user_query: str):

    embed_dependencies = embed_bootstrap.IdentityChunkerHuggingFaceMLE5Embedder()
    embedded_text = embed(chunker=embed_dependencies["chunker"], embedder=embed_dependencies["embedder"], text_data=[user_query])

    content_index_depencencies = content_index_bootstrap.bootstrap()

    results = content_index_services.get_similar_mgoblog_content(uow=content_index_depencencies["uow"], embeddings=[x.embedded_text for x in embedded_text], top_n_results=30)[0]
    for result in results:
        print(f"url: {result.url}; {result.text}")

if __name__ == "__main__":
    user_query("What were some key plays in michigan's game against Northwestern?")
