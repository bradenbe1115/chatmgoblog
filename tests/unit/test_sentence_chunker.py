from embed.common.chunker import SentenceChunker, RecursiveCharacterTextChunker

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

def test_recursive_character_text_chunker():
    with open("/tests/unit/long_text.txt", "r") as file:
        content = file.read()

    chunker = RecursiveCharacterTextChunker()
    results = chunker.chunk_text(content)

    assert len(results) > 0

    results_two = chunker.chunk_text(content, chunk_size=20, chunk_overlap=10)

    assert len(results_two) > len(results)
