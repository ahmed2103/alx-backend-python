def stream_users_in_batches(batch_size):
    seed = __import__('seed')
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    batch = cursor.fetchmany(batch_size)
    while batch:
        yield batch
        batch = cursor.fetchmany(batch_size)

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for row in batch:
            if row[3] > 25:
                print(row)