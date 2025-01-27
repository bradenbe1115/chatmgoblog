import abc
import nltk
from langchain_text_splitters import RecursiveCharacterTextSplitter

nltk.download('punkt_tab')
nltk.download('punkt')

class AbstractChunker(abc.ABC):
    """
        Abstract class for a text chunker to be used to chunk text for embedding.

        Each instance of this class must provide a chunk_text method that implements the given chunking strategy. 
    """

    def chunk_text(self, data: str, **kwargs) -> list[list[str]]:
        """
            Breaks provided text data into chunks using a strategy specific to the class implementation.

            Args:
                data (str): text to be chunked
            Returns:
                A list of lists of strings, where each inner list contains the chunks generated from the corresponding text in the original list.
        """
        return self._chunk_text(data,**kwargs)
    
    @abc.abstractmethod
    def _chunk_text(self, data: str, **kwargs) -> list[list[str]]:
        raise NotImplementedError
    
class SentenceChunker(AbstractChunker):

    def _chunk_text(self, data, **kwargs):
        return nltk.sent_tokenize(data)

class IdentityChunker(AbstractChunker):

    def _chunk_text(self, data, **kwargs):
        return data
    
class RecursiveCharacterTextChunker(AbstractChunker):

    def _chunk_text(self, data, **kwargs):

        chunk_size = kwargs.get("chunk_size", 300)
        chunk_overlap = kwargs.get("chunk_overlap",50)


        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        
        return text_splitter.split_text(data)