from embed import bootstrap as embed_bootstrap
from content_index import bootstrap as content_index_bootstrap

def bootstrap():
    embed_deps = embed_bootstrap.RecursiveTextChunkerHuggingFaceMLE5Embedder()
    content_index_deps = content_index_bootstrap.bootstrap()

    return embed_deps, content_index_deps