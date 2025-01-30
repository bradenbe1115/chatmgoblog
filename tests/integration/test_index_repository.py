from content_index.common import index, models
import numpy as np
import random

def test_chromadb_index_repo(test_chromadb_client):
    repo = index.ChromaDBIndex(test_chromadb_client, content_collection_name="test_collection")

    data = [models.MgoBlogContent(id="1", url="/test", embedding=[0.0, 1.3], text="Test One"),
            models.MgoBlogContent(id="2", url="/test_two", embedding=[-9.2, 1.9], text="Test Two"),
            models.MgoBlogContent(id="3", url="/test_two", embedding=[2.8, 9.9], text="Test Three")]
    
    repo.add_mgoblog_content(content=data)


    retr_test_one = repo.get_mgoblog_content(url="/test")
    assert isinstance(retr_test_one[0], models.MgoBlogContent)
    assert retr_test_one[0].text == "Test One"

    retr_test_two_url_results = repo.get_mgoblog_content(url="/test_two")
    assert len(retr_test_two_url_results) == 2

    repo.delete_mgoblog_content(urls=["/test_two"])
    retr_data_that_should_be_deleted = repo.get_mgoblog_content(url="/test_two")
    assert len(retr_data_that_should_be_deleted) == 0

def test_chromadb_get_similar_content(test_chromadb_client):

    content = []
    for i in range(0,20):
        content.append(models.MgoBlogContent(id=str(i), url=f"/test/{i%5}", embedding=[np.random.normal(i*10,.1),np.random.normal(i*10,.1)], text=f"Test {i}"))
    
    repo = index.ChromaDBIndex(test_chromadb_client, content_collection_name=f"test_collection_{int(random.random()*1000)}")
    repo.add_mgoblog_content(content)

    query_embeddings = [[0,0]]
    similar_results = repo.get_similar_mgoblog_content(embeddings=query_embeddings, top_n_results=10)

    assert len(similar_results[0]) == 10
    
    # Based on distributions, should return the first content entry but not the last -- very very unlikely although it is random
    assert "0" in [x.id for x in similar_results[0]]
    assert "18" not in [x.id for x in similar_results[0]]


    