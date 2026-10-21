import psycopg2
import json
from db.connection import get_connection 
from db.load import load_data


def drop_data():
    
    connection = get_connection()
    cursor = connection.cursor()
    sql_statement = '''DROP TABLE IF EXISTS users;'''

    cursor = connection.cursor()

    cursor.execute(sql_statement)
    connection.commit()
    cursor.close()
    connection.close()

def create_data():
    
    connection = get_connection()
    cursor = connection.cursor()
    sql_statement = '''CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);'''
     
    cursor = connection.cursor()
     
    cursor.execute(sql_statement)
    connection.commit()
    cursor.close()
    connection.close()
  

def insert_data(data):
    connection = get_connection()
    cursor = connection.cursor()
#   {
#     "name": "Alice Rahman",
#     "email": "alice@example.com",
#     "password": "password123"
#   },
    for user in data:
        
        insert_statement = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s);"

        cursor.execute(insert_statement,(user["email"], user["name"], user["password"]))

    connection.commit()

    cursor.close()
    connection.close()


def seed_user_data():
    drop_data()
    create_data()
    data = load_data("db/data/users.json")
    insert_data(data)
        



