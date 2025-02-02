from content_index.common import models, index

def add_mgoblog_content(index: index.AbstractIndex, data: list[dict]) -> None:
    """
        Adds context to indexed database.

        Utilizes an upsert strategy to replace content within index based on url. 
        If content with an incoming URL exists in database, all content associated with that URL will be replaced with the incoming content.

        Args:
            index (AbstractIndex)
            data (list[dict]): data to be inserted into index database. Data will be tested to see if it conforms to index schema for mgoblog content.
    """
    content = [models.MgoBlogContent(**d) for d in data]

    # Drop existing content to be replaced
    unique_urls =list(set([x.url for x in content]))
    index.delete_mgoblog_content(urls=unique_urls)
    
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