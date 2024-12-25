from . import api_client

def test_user_query_happy_path():
    user_query = "What is Bryce Underwood supposed to be good at?"
    r = api_client.get_user_query(user_query)

    assert len(r.json()) > 0
    assert r.json()[0]["url"]