from rag_chat.common import chat_generator
from langchain import hub
from langchain_openai import ChatOpenAI

def bootstrap_chatgpt4_mini():
    prompt = hub.pull("rlm/rag-prompt")
    model = ChatOpenAI(model="gpt-4o-mini")
    chat = chat_generator.LangchainChatGenerator(model=model, prompt=prompt)
    return chat
