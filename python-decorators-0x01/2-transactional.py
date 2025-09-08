import sqlite3
import functools
from warnings import catch_warnings


def with_db_connection(func):
    """ open a connection and closes it as if it is a context manager"""
    @functools.wraps(func)
    def wrapper(user_id):
        connection = sqlite3.connect("users.db")
        result = func(connection, user_id)
        connection.close()
        return result
    return wrapper

def transactional(func):
    """decorator to commit or rollback changes"""
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        try:
            result = func(*args, **kwargs)
            conn = kwargs.get('conn')
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e

    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')