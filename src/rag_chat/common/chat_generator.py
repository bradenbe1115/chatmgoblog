import abc
from rag_chat.common.models import State
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

class AbstractChatGenerator(abc.ABC):
    """
        Base class for a chat generate for RAG application.
    """

    def generate_chat_answer(self, state: State) -> dict:
        """
            Generates a chat answer for RAG application given the current state that's passed in as an argument.

            Parameters:
                state (models.State): a typed dict holding values for the state of the RAG application
            
            Returns:
                a dictionary with a key of "answer" that points to the chat response value
        """

        return self._generate_chat_answer(state)
    
    @abc.abstractmethod
    def _generate_chat_answer(self, state: State) -> dict:
        raise NotImplementedError
    
class LangchainChatGenerator(AbstractChatGenerator):
    """
        Langchain implementation of base class chat generator.

        Parameters:
            model (BaseChatModel): an instantiated BaseChatModel object from langchain core.
            prompt (PromptTemplate): an instantiated PromptTemplate object from langchain core

    """

    def __init__(self, model: BaseChatModel, prompt: PromptTemplate):
        self.model = model
        self.prompt = prompt

    def _generate_chat_answer(self, state) -> dict:
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
        response = self.model.invoke(messages)
        return response.content
