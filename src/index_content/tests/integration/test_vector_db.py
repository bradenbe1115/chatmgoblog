from index_content.common.models import MgoBlogContentEmbedding
from index_content.common.vector_db import ChromaVectorDB

def test_chromadb_vector_db():

    vector = ChromaVectorDB()

    embedding_one = MgoBlogContentEmbedding(id="test_id", url="/test/url/one", embedding=[0,1])
    embedding_two = MgoBlogContentEmbedding(id="test_id_2", url="/test/url/two", embedding=[0,0])

    vector.insert_embedded_mgoblog_content(embeddings=[embedding_one, embedding_two])

    retr_embedding_one = vector.get_embedded_mgoblog_content(id=["test_id"])
    print(retr_embedding_one)
    assert retr_embedding_one['ids'][0] == "/test/url/one"
    assert retr_embedding_one["embeddings"].size > 0