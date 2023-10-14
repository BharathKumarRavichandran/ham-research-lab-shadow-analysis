import os
import pymongo


def get_connection_string():
    protocol = os.environ.get("DB_PROTOCOL", "mongodb")
    username = os.environ["DB_USERNAME"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    if port:
        conn_str = f"{protocol}://{username}:{password}@{host}/?retryWrites=true&w=majority"
    else:
        conn_str = f"{protocol}://{username}:{password}@{host}:{port}/?retryWrites=true&w=majority"
    return conn_str


def create_db_client():
    db_client = pymongo.MongoClient(get_connection_string())
    db = db_client["smart_research"]
    collection = db["shadow_matrix"]
    return db_client, collection
