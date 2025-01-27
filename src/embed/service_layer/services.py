from embed.common import chunker, embedder, models

def embed_content(chunker: chunker.AbstractChunker, embedder: embedder.AbstractEmbedder, text_data: list[dict], text_field_name: str = "text") -> list[models.EmbeddedTextData]:
    """
        Embeds text data using a chunking and embedding algorithm. 

        A chunker algorithm needs to be passed as an argument, as well as an embedder. 

        Function expects a list of dictionaries and will embed only the data in the text field that is passed within each dictionary.
        Key to text field needs to be passed as input (default is 'text').

        Embedded data will be added to the dictionary at the key 'embedded'. If an embedded key-value pair already exists, the value will be overwritten.

        Args:
            chunker: Any chunker class that inherits from the AbstractChunker parent class
            embedder: Any embedder class that inherits from the AbstractEmbedder parent class
            text_data (list(dict)): a list of dicts containing text data to be embedded
            text_field_name (str): name of the key in dictionaries in list to be embedded
    """

    chunked_data = []
    for i in range(0, len(text_data)):
        tmp_dict = text_data[i]
        text_chunks = chunker.chunk_text(text_data[i][text_field_name])
        
        for text_chunk in text_chunks:
            tmp_dict = text_data[i].copy()
            tmp_dict[text_field_name] = text_chunk
            chunked_data.append(tmp_dict)

    embedded_text = embedder.embed_data(data = [x[text_field_name] for x in chunked_data])

    for i in range(0, len(embedded_text)):
        chunked_data[i]['embedded'] = embedded_text[i]

    return chunked_data


