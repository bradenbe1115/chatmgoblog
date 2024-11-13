from embed_data.common.chunker import SentenceChunker

def test_basic_paragraph():
    test_data = ["Hello there. I'm a paragraph of text designed to test a chunker. Isn't working with LLMs fun!", "You have no idea what you are doing. This chunking strategy will never work. Or will it? Only you can figure it out."]

    chunker = SentenceChunker()
    results = chunker.chunk_text(test_data)

    assert len(results[0]) == 3
    assert len(results[1]) == 4
    assert results[1][1] == "This chunking strategy will never work."

def test_paragraph_with_weird_patterns():
    test_data = ["Hello there..... I'm a paragraph of text designed to test a chunker,/n Isn't working with LLMs fun!", "You have no idea what you are doing. This chunking strategy will never work. Or will it? Only you can figure it out."]

    chunker = SentenceChunker()
    results = chunker.chunk_text(test_data)
    assert len(results[0]) == 2