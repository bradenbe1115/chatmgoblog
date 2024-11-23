import os
from chatmgoblog.embeddings.embedder import HuggingFaceInferenceAPIEmbedder
from chatmgoblog.embeddings.embedder import HuggingFaceInferenceAPIInputs

def test_hugging_face_inference_api_embedder_valid_model():
    access_token = os.getenv("HUGGING_FACE_INFERENCE_API_ACCESS_TOKEN")
    model_endpoint = "models/intfloat/multilingual-e5-large-instruct"

    embedder = HuggingFaceInferenceAPIEmbedder(api_inputs=HuggingFaceInferenceAPIInputs(access_token=access_token), model_endpoint = model_endpoint)

    test_data = ["Hello There", "I'm a test string"]
    results = embedder.embed_data(data=test_data)

    assert len(results) == 2
    assert len(results[0]) > 10

def test_hugging_face_inference_api_embedder_invalid_model():
    access_token = os.getenv("HUGGING_FACE_INFERENCE_API_ACCESS_TOKEN")
    model_endpoint = "models/this-is-not-a-model"

    embedder = HuggingFaceInferenceAPIEmbedder(api_inputs=HuggingFaceInferenceAPIInputs(access_token=access_token), model_endpoint = model_endpoint)

    test_data = ["Hello There", "I'm a test string"]
    results = embedder.embed_data(data=test_data)

    assert len(results) == 0
    