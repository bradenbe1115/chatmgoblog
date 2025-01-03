from . import api_client

def test_user_query_happy_path():
    question = "Who made this chat application?"
    context = ["Ben Braden made the chat application", ""]
    r = api_client.get_rag_chat_with_context_response(question=question, context=context)

    print(r.json())
    assert len(r.json()) > 0
    assert r.json()["response"]