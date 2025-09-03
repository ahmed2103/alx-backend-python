import mysql.connector
import uuid
import csv
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password = 'none'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("no connection",e)
        return None

def create_database(connection):
    """create database if not exist"""
    cursor = connection.cursor()
    cursor.execute('create database if not exists ALX_prodev')
    print("database created successfully")
    cursor.close()

def connect_to_prodev():
    """connect to database"""
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='none',
            database='ALX_prodev'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("can't connect to database")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    create table if not exists user_data(
    user_id char(36) primary key,
    name varchar(50) not null,
    email varchar(50) not null,
    age decimal(4,1) not null)
    """)
    print("user_data table created successfully")
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.execute('select count(*) from user_data')
    count = cursor.fetchone()[0]
    if count > 0:
        print("data already exist")
        cursor.close()
        return

    with open('data.csv','r', newline='', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        insert_query = """insert into user_data (user_id, name, email, age) values (%s,%s,%s,%s)"""
        for row in csv_reader:
            user_id = str(uuid.uuid4())
            name = row.get('name')
            email = row.get('email')
            age = int(row.get('age'))

            cursor.execute(insert_query, (user_id,name,email,age))
    connection.commit()
    cursor.close()

