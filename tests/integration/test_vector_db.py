from embed_data.common.models import MgoBlogContentEmbedding
from embed_data.common.vector_db import ChromaVectorDB

def test_chromadb_vector_db():

    vector = ChromaVectorDB()

    embedding_one = MgoBlogContentEmbedding(url="/test/url/one", embedding=[0,1])
    embedding_two = MgoBlogContentEmbedding(url="/test/url/two", embedding=[0,0])

    vector.insert_embedded_mgoblog_content(embeddings=[embedding_one, embedding_two])

    retr_embedding_one = vector.get_embedded_mgoblog_content(urls=["/test/url/one"])
    print(retr_embedding_one)
    assert retr_embedding_one['ids'][0] == "/test/url/one"
    assert retr_embedding_one["embeddings"].size > 0