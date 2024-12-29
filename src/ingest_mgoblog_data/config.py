import os

DB_URI = "elt_db"
PORT = 27017

def get_mongo_db_info() -> tuple[str, int]:
    db_uri = os.environ.get("ELT_DB_URI", DB_URI)
    port = os.environ.get("ELT_DB_PORT", PORT)
    return db_uri ,port