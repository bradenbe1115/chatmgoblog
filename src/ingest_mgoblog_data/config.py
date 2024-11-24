import os

DB_URI = "elt_db"

port = 27017

def get_mongo_db_info() -> tuple[str, int]:
    db_uri = os.environ.get("ELT_DB_URI", "elt_db")
    port = os.environ.get("ELT_DB_PORT", 27017)
    return db_uri ,port