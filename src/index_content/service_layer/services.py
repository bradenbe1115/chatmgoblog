from index_content.common import chunker, embedder, models


def embed(chunker: chunker.AbstractChunker, embedder: embedder.AbstractEmbedder, text_data: list[str]) -> list[models.EmbeddedTextData]:

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


