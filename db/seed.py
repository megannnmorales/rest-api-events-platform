import psycopg2
import json
from db.connection import get_connection 
from db.load import load_data


def drop_data():
    
    connection = get_connection()
    cursor = connection.cursor()
    sql_statement = '''DROP TABLE IF EXISTS venues;
    DROP TABLE IF EXISTS users;
    '''

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
    created_at TIMESTAMPTZ DEFAULT NOW());

    CREATE TABLE venues (
    venue_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address text,
    capacity INT);
    ''' 
     
    cursor.execute(sql_statement)
    connection.commit()
    cursor.close()
    connection.close()
  

def insert_user_data(user_data):
    connection = get_connection()
    cursor = connection.cursor()

    for user in user_data:
        
        insert_statement = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s);"

        cursor.execute(insert_statement,(user["email"], user["name"], user["password"]))

    connection.commit()

    cursor.close()
    connection.close()

def insert_venue_data(venue_data):
    connection = get_connection()
    cursor = connection.cursor()

    for venue in venue_data:
            
            insert_statement = "INSERT INTO venues(name, address, capacity) VALUES (%s, %s, %s);"
    
            cursor.execute(insert_statement,(venue["name"], venue["address"], venue["capacity"]))

    connection.commit()

    cursor.close()
    connection.close()

def seed_data():
    drop_data()
    create_data()
    user_data = load_data("db/data/users.json")
    venue_data = load_data("db/data/venues.json")
    insert_user_data(user_data)
    insert_venue_data(venue_data)
        

