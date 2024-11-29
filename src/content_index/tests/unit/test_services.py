from content_index.service_layer import services, unit_of_work
from content_index.common import models, index_repository

class FakeIndex(index_repository.AbstractIndexRepository):

    def __init__(self):
        super().__init__()
        self._index = set()

    def _add_mgoblog_content(self, content):
        for c in content:
            self._index.add(c)
        
    
    def _get_mgoblog_content(self, url):
        results = [r for r in self._index if r.url == url]
        return results
    
class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.index = FakeIndex()

def test_add_mgoblog_content():
    uow = FakeUnitOfWork()
    services.add_mgoblog_content(uow=uow, data=[{"id": "test_one", "url": "test_url/one", "embedding":[0.0], "text": "test one"}])

    assert len(uow.index._index) 

def test_get_mgoblog_content_by_url():
    uow = FakeUnitOfWork()
    uow.index._index.add(models.MgoBlogContent(id="test_one", embedding=[0.0], text="test one", url="test_url/one"))
    results = services.get_mgoblog_content_by_url(uow=uow, url="test_url/one")
    assert len(results) == 1
