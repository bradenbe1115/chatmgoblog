import requests

def get_user_query(user_query):
    url = "http://user_query_api:80"
    r = requests.get(
        f"{url}/user_query", json={"user_query": user_query}
    )
    assert r.status_code == 200
    return r