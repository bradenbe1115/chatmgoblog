from embed.common import chunker, embedder, models


def embed(chunker: chunker.AbstractChunker, embedder: embedder.AbstractEmbedder, text_data: list[str]) -> list[models.EmbeddedTextData]:
    """
        Takes a list of text data as input and embeds it using a LLM model.

        Embedded data is returned in a class with shared attributes. Since data is chunked during embedding process, it's common for the
        length of the return data to be longer than the input data, depending on the type of chunking method used and the details of the input data.

        The original index of the data is included in the returned objects for processing purposes.

        Args:
            chunker: Any chunker class that inherits from the AbstractChunker parent class
            embedder: Any embedder class that inherits from the AbstractEmbedder parent class
    """

    chunked_data = [
        {"index": i, "text": text}
        for i in range(0,len(text_data))
        for j, text in enumerate(chunker.chunk_text(text_data[i]))
    ]

    embedded_text = embedder.embed_data(data = [x["text"] for x in chunked_data])

    embedded_data = []
    for i in range(0, len(embedded_text)):
        embedded_data.append(models.EmbeddedTextData(index=chunked_data[i]["index"], text=chunked_data[i]["text"], embedded_text=embedded_text[i]))
    
    return embedded_data


