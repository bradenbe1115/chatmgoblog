import abc
import chromadb

from content_index.common import models


class AbstractIndexRepository(abc.ABC):

    def add_mgoblog_content(self, content: list[models.MgoBlogContent]) -> None:
        """
        Adds Mgoblog content to an indexed database for efficient retrievel of embedded content.

        Args:
            content (list[models.MgoBlogContent])
        """
        self._add_mgoblog_content(content=content)

    @abc.abstractmethod
    def _add_mgoblog_content(self, content: list[models.MgoBlogContent]) -> None:
        raise NotImplementedError

    def get_mgoblog_content(self, url: str) -> list[models.MgoBlogContent]:
        """
        Returns a list of Mgoblog content with matching url from indexed database.

        Args:
            url (str)
        """
        return self._get_mgoblog_content(url)

    @abc.abstractmethod
    def _get_mgoblog_content(self, url: str) -> list[models.MgoBlogContent]:
        raise NotImplementedError


class ChromaDBIndexRepository(AbstractIndexRepository):

    def __init__(self, client: chromadb.HttpClient):
        self.client = client

    def _get_create_collection(self, collection_name: str):
        """
        Gets a collection, creates it if it doesn't exist already
        """
        return self.client.create_collection(name=collection_name, get_or_create=True)

    def _add_mgoblog_content(self, content: list[models.MgoBlogContent]):
        mgoblog_content_collection = self._get_create_collection(
            collection_name="mgoblog_content_embeddings"
        )
        mgoblog_content_collection.add(
            ids=[x.id for x in content],
            embeddings=[x.embedding for x in content],
            metadatas=[{"url": x.url} for x in content],
            documents=[x.text for x in content],
        )

    def _get_mgoblog_content(self, url: str) -> list[models.MgoBlogContent]:
        mgoblog_content_collection = self._get_create_collection(
            collection_name="mgoblog_content_embeddings"
        )

        
        results = mgoblog_content_collection.get(where={"url":url}, include=["embeddings", "documents", "metadatas"])
        
        final_results = []
        for i in range(0,len(results["ids"])):
            final_results.append(models.MgoBlogContent(id=results["ids"][i], url=results["metadatas"][i]["url"], embedding=results["embeddings"][i], text=results["documents"][i]))

        return final_results
