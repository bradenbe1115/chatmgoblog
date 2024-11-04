from ingest_mgoblog_data.common.repository import PyMongoMgoBlogContentRepository
from ingest_mgoblog_data.common.models import MgoblogContentLandingDataSchema

DB_URI = "landing_db"
DB_NAME = "test_db"
RAW_DATA_COLLECTION_NAME = "test_repository"

def test_mgoblog_content_repository():
    repo = PyMongoMgoBlogContentRepository(db_uri=DB_URI, database_name=DB_NAME, raw_mgoblog_content_collection_name=RAW_DATA_COLLECTION_NAME)

    data = [MgoblogContentLandingDataSchema(url="/url_one", raw_html="Hello World", date_collected="2024-01-01"),
            MgoblogContentLandingDataSchema(url="/url_two", raw_html="Hello World Again", date_collected="2024-02-01")]
    
    repo.add_raw_mgoblog_content(data=data)

    retr_entry = repo.get_raw_mgoblog_content(url="/url_one")
    assert retr_entry is not None
    assert retr_entry["raw_html"] == "Hello World"
    assert repo.get_raw_mgoblog_content(url="/url_two") is not None

    new_data = [MgoblogContentLandingDataSchema(url="/url_one", raw_html="Hello World - Test Update", date_collected="2024-01-01")]

    repo.add_raw_mgoblog_content(new_data)
    retr_entry = repo.get_raw_mgoblog_content(url="/url_one")
    assert retr_entry is not None
    assert retr_entry["raw_html"] == "Hello World - Test Update"