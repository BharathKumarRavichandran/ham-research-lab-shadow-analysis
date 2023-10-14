import os


def get_connection_string():
    username = os.environ["DB_USERNAME"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    conn_str = f"mongodb://{username}:{password}@{host}:{port}/"
    return conn_str
