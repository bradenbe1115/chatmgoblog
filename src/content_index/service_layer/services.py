from content_index.common import models, index

def add_mgoblog_content(index: index.AbstractIndex, data: list[dict]) -> None:
    content = [models.MgoBlogContent(**d) for d in data]

    index.add_mgoblog_content(content)


def get_mgoblog_content_by_url(index: index.AbstractIndex, url: str) -> list[models.MgoBlogContent]:

    retr_content = index.get_mgoblog_content(url=url)

    return retr_content

def get_similar_mgoblog_content(index: index.AbstractIndex, embeddings: list[list[float]], top_n_results: int) -> list[models.MgoBlogContent]:

    retr_content = index.get_similar_mgoblog_content(embeddings=embeddings, top_n_results=top_n_results)

    return retr_content

def list_mgoblog_content(index: index.AbstractIndex) -> list[models.MgoBlogContent]:
    retr_content = index.list_mgoblog_content()
    
    return retr_content