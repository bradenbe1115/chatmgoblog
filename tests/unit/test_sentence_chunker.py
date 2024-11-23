from chatmgoblog.embeddings.chunker import SentenceChunker

def test_basic_paragraph():
    test_data = "Hello there. I'm a paragraph of text designed to test a chunker. Isn't working with LLMs fun!"

    chunker = SentenceChunker()
    results = chunker.chunk_text(test_data)

    assert len(results) == 3
    assert results[1] == "I'm a paragraph of text designed to test a chunker."

def test_paragraph_with_weird_patterns():
    test_data = "Hello there..... I'm a paragraph of text designed to test a chunker,/n Isn't working with LLMs fun!"

    chunker = SentenceChunker()
    results = chunker.chunk_text(test_data)
    assert len(results) == 2