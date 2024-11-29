from content_index.service_layer import services, unit_of_work
from content_index.common import models, index_repository
import random
import string

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
    
    def _get_similar_mgoblog_content(self, embeddings, top_n_results):
        return list(random.sample(self._index,min(top_n_results, len(self._index))))
    
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

def test_get_similar_mgoblog_content():

    uow = FakeUnitOfWork()

    for i in range(0, 10):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        content = models.MgoBlogContent(id=f"test_{random_string}", embedding=[random.random(), random.random()], text=random_string, url=f"url/{random_string}")

        uow.index._index.add(content)
    
    results = services.get_similar_mgoblog_content(uow=uow, embeddings=[[0.0]], top_n_results=3)
    assert len(results) == 3
