def stream_user_ages():
    seed = __import__('seed')
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row[3]

def get_age_average():
    count = 0
    sum = 0
    for age in stream_user_ages():
        sum += age
        count +=1
    return sum / count

print(f' Average age of users: {get_age_average()}')