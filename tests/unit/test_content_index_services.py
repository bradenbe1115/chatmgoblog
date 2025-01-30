from content_index.service_layer import services
from content_index.common import index, models
import random
import string

class FakeIndex(index.AbstractIndex):

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
    
    def _delete_mgoblog_content(self, urls):
        self._index = {x for x in self._index if x.url in urls}
    
    def _list_mgoblog_content(self):
        return list(self._index)

def test_add_mgoblog_content():
    index = FakeIndex()
    services.add_mgoblog_content(index=index, data=[{"id": "test_one", "url": "test_url/one", "embedding":[0.0], "text": "test one"}])

    assert len(index._index) 

def test_get_mgoblog_content_by_url():
    index = FakeIndex()
    index._index.add(models.MgoBlogContent(id="test_one", embedding=[0.0], text="test one", url="test_url/one"))
    results = services.get_mgoblog_content_by_url(index=index, url="test_url/one")
    assert len(results) == 1

def test_get_similar_mgoblog_content():

    index = FakeIndex()

    for i in range(0, 10):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        content = models.MgoBlogContent(id=f"test_{random_string}", embedding=[random.random(), random.random()], text=random_string, url=f"url/{random_string}")

        index._index.add(content)
    
    results = services.get_similar_mgoblog_content(index=index, embeddings=[[0.0]], top_n_results=3)
    assert len(results) == 3
