from index_content.common import embedder, chunker
from index_content.service_layer import services
import random

class FixedSequenceChunker(chunker.AbstractChunker):
    
    def __init__(self, chunk_size=5):
        self.chunk_size = chunk_size

    def _chunk_text(self, data):
        return [data[i:i + self.chunk_size] for i in range(0, len(data), self.chunk_size)]
    
class FakeEmbedder(embedder.AbstractEmbedder):

    def _embed_data(self, data):
        
        return [[random.random(), random.random()] for d in data]

def test_embed_service():

    chunker = FixedSequenceChunker()
    embedder = FakeEmbedder()

    results = services.embed(chunker=chunker, embedder=embedder, text_data=["abcdefghij", "klmnopqrst"])

    assert len(results) == 4
    assert results[0].text == "abcde"
    assert len(results[0].embedded_text) == 2
    assert results[0].index == 0
    assert results[1].index == 0
    assert results[-1].index == 1