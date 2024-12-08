import abc

from pydantic import BaseModel
import requests

class AbstractEmbedder(abc.ABC):
    """
        Abstract embedding interface that can be used to convert strings into vector embeddings.
    """

    def embed_data(self, data: list[str])-> list[list[float]]:
        """
            Takes a list of strings and converts it into vector embeddings.

            Implementation details are dependent on specific abstraction being used

            Parameters:
                data (list[str]): list of strings that will be converted to embeddings

            Returns:
                list of embeddings, which are represented as a list of floats

        """
        return self._embed_data(data)
    
    @abc.abstractmethod
    def _embed_data(self, data: list[str]) -> list[list[int]]:
        raise NotImplementedError
    
class HuggingFaceInferenceAPIInputs(BaseModel):
    access_token: str
    
class HuggingFaceInferenceAPIEmbedder(AbstractEmbedder):
    base_url = "https://api-inference.huggingface.co"
    """
        Embedder interface implemented using the Hugging Face Inference API.

        The Hugging Face Inference API exposes community built Gen AI models that can be accessed via a bearer token.

        API inputs must be passed upon initialization and will be used in all calls to the embed_data method. 
    """

    def __init__(self, api_inputs: HuggingFaceInferenceAPIInputs, model_endpoint: str):
        """
            Parameters:
                api_inputs (HuggingFaceInferenceAPIInputs): Hugging Face Inference API inputs
                model_endpoint (str): endpoint for embedding model to use. Expected format is to not start with a '/'. Example: "models/intfloat/multilingual-e5-large-instruct"
        """
        self.api_inputs = api_inputs
        self.model_endpoint = model_endpoint

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.api_inputs.access_token}", "x-wait-for-model":"true"}
    
    def _embed_data(self, data: list[str], chunk_size:int=100) -> list[list[int]]:

        results = []
        for i in range(0,len(data),chunk_size):
            payload = {"inputs": data[i:i+chunk_size]}

            response = requests.post(f"{self.base_url}/{self.model_endpoint}", headers=self.headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                results += result
            else:
                print(f"Failed to successfully retrieve embedded vector. Received status code: {response.status_code}; Error Message: {response.text}")
        
        if len(results) > 0:
            return results
        
        else:
            raise RuntimeError("Unable to embed data successfully.")
        