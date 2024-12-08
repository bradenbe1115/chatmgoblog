from embed.common import embedder, chunker
from embed import config

def SentenceChunkerHuggingFaceMLE5Embedder():

    ch = chunker.SentenceChunker()
    em = embedder.HuggingFaceInferenceAPIEmbedder(api_inputs=config.get_hugging_face_api_creds(), model_endpoint="models/intfloat/multilingual-e5-large-instruct")

    return {"embedder": em, "chunker": ch}

def IdentityChunkerHuggingFaceMLE5Embedder():

    ch = chunker.IdentityChunker()
    em = embedder.HuggingFaceInferenceAPIEmbedder(api_inputs=config.get_hugging_face_api_creds(), model_endpoint="models/intfloat/multilingual-e5-large-instruct")

    return {"embedder": em, "chunker": ch}
