from embed_data.common import embedder
from embed_data.common import vector_db
from ingest_mgoblog_data.common import models
from ingest_mgoblog_data.common import repository
from ingest_mgoblog_data.common import web_scraper

class FakeMgoBlogContentRepository(repository.AbstractMgoBlogContentRepository):
    
    def __init__(self):
        self._raw_content = set()
        self._processed_content = set()

    def _add_raw_mgoblog_content(self, mgoblog_content_landing_data):
        self._raw_content.add(mgoblog_content_landing_data)
    
    def _get_raw_mgoblog_content(self, url):
        return next((d for d in self._raw_content if d.url == url), None)
    
    def _add_processed_mgoblog_content(self, mgoblog_processed_data):
        self._processed_content.add(mgoblog_processed_data)
    
    def _get_processed_mgoblog_content(self, url):
        return next((d for d in self._processed_content if d.url == url), None)
    
class FakeEmbedder(embedder.AbstractEmbedder):

    def _embed_data(self, data):
        results = []
        for d in data:
            result = []
            result.append(len(d), d.count(' '))
            results.append(result)
        
        return results
    
class FakeVectorDB(vector_db.AbstractVectorDB):

    def __init__(self):
        self._embedded_mgoblog_content = set()

    def _insert_embedded_mgoblog_content(self, embeddings):
        self._insert_embedded_mgoblog_content(embeddings)
        return
    
    def _get_embedded_mgoblog_content(self, urls):
        results = []
        for content in self._embedded_mgoblog_content:
            if content.url in urls:
                results.append(content)
        return results