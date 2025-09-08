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

def retry_on_failure(retries=3, delay=1):
    """retries the query if there exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for retry in range(retries+1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if retry > retries:
                        time.sleep(delay)
                    else:
                        raise e

        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)