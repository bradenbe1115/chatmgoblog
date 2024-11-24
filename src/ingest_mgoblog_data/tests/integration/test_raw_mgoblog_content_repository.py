from ingest_mgoblog_data.common.repository import PyMongoMgoBlogContentRepository
from ingest_mgoblog_data.common.models import MgoblogContentLandingDataSchema

def test_mgoblog_content_repository(test_elt_db_client):
    client = test_elt_db_client
    repo = PyMongoMgoBlogContentRepository(client)

    data = [MgoblogContentLandingDataSchema(url="/url_one", raw_html="Hello World", collected_ts=1234),
            MgoblogContentLandingDataSchema(url="/url_two", raw_html="Hello World Again", collected_ts=1234)]
    
    repo.add_raw_mgoblog_content(mgoblog_content_landing_data=data)

    retr_entry = repo.get_raw_mgoblog_content(url="/url_one")
    assert retr_entry is not None
    assert retr_entry.raw_html == "Hello World"
    assert repo.get_raw_mgoblog_content(url="/url_two") is not None

    new_data = [MgoblogContentLandingDataSchema(url="/url_one", raw_html="Hello World - Test Update", collected_ts=1234)]

    repo.add_raw_mgoblog_content(new_data)
    retr_entry = repo.get_raw_mgoblog_content(url="/url_one")
    assert retr_entry is not None
    assert retr_entry.raw_html == "Hello World - Test Update"