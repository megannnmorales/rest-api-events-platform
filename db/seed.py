import psycopg2
import json
from db.connection import get_connection 
from db.load import load_data


def drop_data(cursor):
    
    drop_sql_statement = '''DROP TABLE IF EXISTS rsvps; 
    DROP TABLE IF EXISTS events;
    DROP TABLE IF EXISTS venues;
    DROP TABLE IF EXISTS users;
    '''

    cursor.execute(drop_sql_statement)

def create_data(cursor):
    
    sql_statement = '''CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE venues (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address text,
        capacity INT
    );

    CREATE TABLE events (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(255),
        starts_at TIMESTAMPTZ NOT NULL,
        ends_at TIMESTAMPTZ NOT NULL,
        organiser_id INT REFERENCES users(id) NOT NULL,
        venue_id INT REFERENCES venues(id) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE TABLE rsvps (
        id SERIAL PRIMARY KEY,
        attendee_id INT REFERENCES users(id) NOT NULL,
        event_id INT REFERENCES events(id) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    '''  
    cursor.execute(sql_statement)

  

def insert_user_data(user_data, cursor):

    for user in user_data:
        
        insert_statement = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s);"

        cursor.execute(insert_statement,(user["email"], user["name"], user["password"]))


def insert_venue_data(venue_data, cursor):

    for venue in venue_data:
        insert_statement = "INSERT INTO venues(name, address, capacity) VALUES (%s, %s, %s);"
    
        cursor.execute(insert_statement,(venue["name"], venue["address"], venue["capacity"]))

def insert_event_data(events_data, cursor):

    for event in events_data:
            
        insert_statement = "INSERT INTO events(title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s);"
    
        cursor.execute(insert_statement,(event["title"], event["description"], event["starts_at"], event["ends_at"], event["organiser_id"], event["venue_id"]))

def insert_rsvp_data(rsvp_data, cursor):

    for rsvp in rsvp_data:
            
        insert_statement = "INSERT INTO rsvps(attendee_id, event_id) VALUES (%s, %s);"
    
        cursor.execute(insert_statement,(rsvp["attendee_id"], rsvp["event_id"]))   

def seed_data():
    connection = get_connection()
    cursor = connection.cursor()

    try: 
        drop_data(cursor)
        create_data(cursor)
        user_data = load_data("db/data/development/users.json")
        venue_data = load_data("db/data/development/venues.json")
        event_data = load_data("db/data/development/events.json")
        rsvp_data = load_data("db/data/development/rsvps.json")
        insert_user_data(user_data, cursor)
        insert_venue_data(venue_data, cursor)
        insert_event_data(event_data, cursor)
        insert_rsvp_data(rsvp_data, cursor)
        connection.commit()
    finally:
        cursor.close()
        connection.close()    

