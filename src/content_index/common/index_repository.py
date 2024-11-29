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
    
    def get_mgoblog_content(self, url: str) -> list[models.MgoBlogContent]:
        """
        Returns a list of Mgoblog content with matching url from indexed database.

        Args:
            url (str)
        """
        return self._get_mgoblog_content(url)
    
    def get_similar_mgoblog_content(self, embeddings: list[list[float]], top_n_results:int = 5) -> list[models.MgoBlogContent]:
        """
            Returns the n most similar Mgoblog content pieces in the database based on embedding similarity.

            Args:
                embeddings (list[list[float]]): a list of embeddings that will be used to query against the database for similarity
                top_n_results (int): number of results to return from database
        """
        return self._get_similar_mgoblog_content(embeddings, top_n_results)

    @abc.abstractmethod
    def _add_mgoblog_content(self, content: list[models.MgoBlogContent]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_mgoblog_content(self, url: str) -> list[models.MgoBlogContent]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get_similar_mgoblog_content(self, embeddings: list[list[float]], top_n_results: int) -> list[models.MgoBlogContent]:
        raise NotImplementedError


class ChromaDBIndexRepository(AbstractIndexRepository):
    field_include_list = ["embeddings", "documents", "metadatas"]

    def __init__(self, client: chromadb.HttpClient, content_collection_name: str= "mgoblog_content_embeddings"):
        self.client = client
        self.content_collection_name = content_collection_name

    @property
    def mgoblog_content_collection(self):
        return self.client.create_collection(name=self.content_collection_name, get_or_create=True)
    
    def _parse_chromadb_get_results(self, results: dict) -> list[models.MgoBlogContent]:
        """
            Parses results from chromadb client get request into a list of MgoBlogContent objects
        """
        final_results = []
        for i in range(0, len(results["ids"])):
            final_results.append(models.MgoBlogContent(id=results["ids"][i], url=results["metadatas"][i]["url"], embedding=results["embeddings"][i], text=results["documents"][i]))

        return final_results
    
    def _parse_chromadb_query_results(self, results: dict) -> list[models.MgoBlogContent]:
        """
            Parses results from chromadb client query request into a list of MgoBlogContent objects
        """
        final_results = []
        for i in range(0, len(results["ids"])):
            interm_result = []
            for j in range(0, len(results["ids"][i])):
                interm_result.append(models.MgoBlogContent(id=results["ids"][i][j], url=results["metadatas"][i][j]["url"], embedding=results["embeddings"][i][j], text=results["documents"][i][j]))
            final_results.append(interm_result)

        return final_results

    def _add_mgoblog_content(self, content: list[models.MgoBlogContent]):
        
        self.mgoblog_content_collection.add(
            ids=[x.id for x in content],
            embeddings=[x.embedding for x in content],
            metadatas=[{"url": x.url} for x in content],
            documents=[x.text for x in content],
        )

    def _get_mgoblog_content(self, url: str) -> list[models.MgoBlogContent]:

        results = self.mgoblog_content_collection.get(where={"url":url}, include=self.field_include_list)
        
        final_results = self._parse_chromadb_get_results(results = results)
        return final_results
    
    def _get_similar_mgoblog_content(self, embeddings, top_n_results) -> list[list[models.MgoBlogContent]]:
        results = self.mgoblog_content_collection.query(query_embeddings=embeddings, n_results=top_n_results, include=self.field_include_list)
        final_results = self._parse_chromadb_query_results(results=results)
        return final_results
