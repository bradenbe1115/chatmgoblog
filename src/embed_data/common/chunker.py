import abc
import nltk

nltk.download('punkt_tab')
nltk.download('punkt')

class AbstractChunker(abc.ABC):
    """
        Abstract class for a text chunker to be used to chunk text for embedding.

        Each instance of this class must provide a chunk_text method that implements the given chunking strategy. 
    """

    def chunk_text(self, data: str) -> list[list[str]]:
        """
            Breaks provided text data into chunks using a strategy specific to the class implementation.

            Args:
                data (str): text to be chunked
            Returns:
                A list of lists of strings, where each inner list contains the chunks generated from the corresponding text in the original list.
        """
        return self._chunk_text(data)
    
    @abc.abstractmethod
    def _chunk_text(self, data: str) -> list[list[str]]:
        raise NotImplementedError
    
class SentenceChunker(AbstractChunker):

    def _chunk_text(self, data):
        return nltk.sent_tokenize(data)

    
def chunk_text(data: str):

    chunker = SentenceChunker()

    result = chunker.chunk_text(data)

    return result