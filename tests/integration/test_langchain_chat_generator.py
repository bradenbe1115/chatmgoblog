from rag_chat.common.chat_generator import LangchainChatGenerator
from rag_chat.common.models import State
from langchain_core.documents import Document
from langchain import hub

def test_chat_generator(langchain_model):

    prompt = hub.pull("rlm/rag-prompt")

    chat = LangchainChatGenerator(model=langchain_model, prompt=prompt)
    documents = [Document(page_content="This is a RAG Application created by Ben Braden"), Document(page_content="It was definitely not created by Jon Lorenz")]
    state = State(question="Who created the RAG application?", context=documents, answer="")

    response = chat.generate_chat_answer(state)
    assert response is not None
    print(response)
    assert len(response) > 0
    assert "Ben Braden" in response