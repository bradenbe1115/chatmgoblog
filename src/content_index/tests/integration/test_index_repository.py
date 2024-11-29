from content_index.common import index_repository, models

def test_chromadb_index_repo(test_chromadb_client):
    repo = index_repository.ChromaDBIndexRepository(test_chromadb_client)

    data = [models.MgoBlogContent(id="1", url="/test", embedding=[0.0, 1.3], text="Test One"),
            models.MgoBlogContent(id="2", url="/test_two", embedding=[-9.2, 1.9], text="Test Two"),
            models.MgoBlogContent(id="3", url="/test_two", embedding=[2.8, 9.9], text="Test Three")]
    
    repo.add_mgoblog_content(content=data)


    retr_test_one = repo.get_mgoblog_content(url="/test")
    assert isinstance(retr_test_one[0], models.MgoBlogContent)
    assert retr_test_one[0].text == "Test One"

    retr_test_two_url_results = repo.get_mgoblog_content(url="/test_two")
    assert len(retr_test_two_url_results) == 2