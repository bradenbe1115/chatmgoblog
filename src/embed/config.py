import os
from embed.common import embedder


def get_hugging_face_api_creds() -> embedder.HuggingFaceInferenceAPIInputs:
    api_token = os.environ.get("HUGGING_FACE_INFERENCE_API_ACCESS_TOKEN",None)
    return embedder.HuggingFaceInferenceAPIInputs(access_token=api_token)