import abc
import chromadb

from index_content.common.models import MgoBlogContentEmbedding

class AbstractVectorDB(abc.ABC):

    def insert_embedded_mgoblog_content(self, embeddings: list[MgoBlogContentEmbedding]):
        self._insert_embedded_mgoblog_content(embeddings)

    @abc.abstractmethod
    def _insert_embedded_mgoblog_content(self, embeddings: list[MgoBlogContentEmbedding]):
        raise NotImplementedError

    
class ChromaVectorDB(AbstractVectorDB):

    def __init__(self, host='http://vector_db:6333', port=6333):
        self.host = host
        self.port = port

    @property
    def client(self):
        try:
            return self._client
        
        except AttributeError:
            self._client = chromadb.HttpClient(host=self.host, port=self.port)
            return self._client
        
    def _get_create_collection(self, collection_name: str):
        """
            Gets a collection, creates it if it doesn't exist already
        """
        return self.client.create_collection(name=collection_name, get_or_create=True)

    
    def _insert_embedded_mgoblog_content(self, embeddings: list[MgoBlogContentEmbedding]):
        mgoblog_content_collection = self._get_create_collection(collection_name="mgoblog_content_embeddings")
        mgoblog_content_collection.add(ids=[x.id for x in embeddings], embeddings=[x.embedding for x in embeddings])

    def get_embedded_mgoblog_content(self, ids: list[str]):
        """
            Method to retrieve content embeddings based on id list input. Main purpose of this method is to test and ensure
            insert content is in database.
        """
        mgoblog_content_collection = self._get_create_collection(collection_name="mgoblog_content_embeddings")
        return mgoblog_content_collection.get(ids=ids, include=['embeddings'])
