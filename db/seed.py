import psycopg2
import json
from db.connection import get_connect 


def drop_data():
    
    connection = get_connect()
    sql_statement = '''DROP TABLE IF EXISTS users;'''

    cursor = connection.cursor()

    cursor.execute(sql_statement)
    cursor.close()
    connection.close()
    pass

def create_data():
    connection = get_connect()
    sql_statement = '''CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);'''
     
    cursor = connection.cursor()
     
    cursor.execute(sql_statement)

    cursor.close()
    connection.close()
    pass

def load_data(filepath):

    with open(filepath) as file:

        data = json.load(file)
    return data



