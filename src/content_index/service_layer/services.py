from content_index.service_layer import unit_of_work
from content_index.common import models

def add_mgoblog_content(uow: unit_of_work.AbstractUnitOfWork, data: list[dict]) -> None:
    content = [models.MgoBlogContent(**d) for d in data]

    with uow:
        uow.index.add_mgoblog_content(content)


def get_mgoblog_content_by_url(uow: unit_of_work.AbstractUnitOfWork, url: str) -> list[models.MgoBlogContent]:

    with uow:
        retr_content = uow.index.get_mgoblog_content(url=url)

    return retr_content

def get_similar_mgoblog_content(uow: unit_of_work.AbstractUnitOfWork, embeddings: list[list[float]], top_n_results: int) -> list[models.MgoBlogContent]:

    with uow:
        retr_content = uow.index.get_similar_mgoblog_content(embeddings=embeddings, top_n_results=top_n_results)

    return retr_content