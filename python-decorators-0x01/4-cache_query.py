import time
import sqlite3
import functools

def with_db_connection(func):
    """ open a connection and closes it as if it is a context manager"""
    @functools.wraps(func)
    def wrapper(user_id):
        connection = sqlite3.connect("users.db")
        result = func(connection, user_id)
        connection.close()
        return result
    return wrapper

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(query, *args,**kwargs):
        result = func(query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")