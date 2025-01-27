from rag_chat.common import chat_generator, models
from langchain_core.documents import Document

def generate_chat_response_with_context(question: str, context: list[str], chat: chat_generator.AbstractChatGenerator) -> str:
    
    context_docs = [Document(page_content=x) for x in context]
    state = models.State(question=question, context=context_docs)

    response = chat.generate_chat_answer(state)

    return response