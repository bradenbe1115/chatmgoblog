from ingest_mgoblog_data.service_layer import services, unit_of_work
from ingest_mgoblog_data.common import repository, models

class FakeRepository(repository.AbstractMgoBlogContentRepository):

    def __init__(self):
        super().__init__()
        self._raw_content = set()
        self._processed_content = set()
        self.data_processed = False

    def _add_raw_mgoblog_content(self, mgoblog_content_landing_data):
        for data in mgoblog_content_landing_data:
            self._raw_content.add(data)

    def _add_processed_mgoblog_content(self, mgoblog_processed_data):
        for data in mgoblog_processed_data:
            self._processed_content.add(data)
        self.data_processed = True
    
    def _get_raw_mgoblog_content(self, urls):
        results = [r for r in self._raw_content if r.url in urls]
        return results

    def _list_mgoblog_content(self):
        results = [r for r in self._raw_content]
        return results


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.content = FakeRepository()

def test_process_mgoblog_data():
    raw_content = models.MgoblogContentLandingDataSchema(url="test_url/", raw_html="<html></html>", collected_ts=1234)
    raw_content_2 = models.MgoblogContentLandingDataSchema(url="test_url/2", raw_html="<html></html>", collected_ts=1234)
    uow = FakeUnitOfWork()
    uow.content.add_raw_mgoblog_content([raw_content, raw_content_2])

    services.process_mgoblog_data(uow=uow, event={"landed_urls":["test_url/"]})

    assert uow.content.data_processed

