def stream_users():
    seed = __import__('seed')
    connection = seed.connect_to_prodev()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    row = cursor.fetchone()
    while row is not None:
        yield row
        row = cursor.fetchone()
from itertools import islice

# iterate over the generator function and print only the first 6 rows

for user in islice(stream_users(), 6):
    print(user)