from db.seed import drop_data, create_data, insert_user_data, insert_venue_data, insert_event_data, insert_rsvp_data 
from db.connection import get_connection
from db.load import load_data

def seed_test_data():
    connection = get_connection()
    cursor = connection.cursor()

    try: 
        drop_data(cursor)
        create_data(cursor)
        user_data = load_data("db/data/test/users.json")
        venue_data = load_data("db/data/test/venues.json")
        event_data = load_data("db/data/test/events.json")
        rsvp_data = load_data("db/data/test/rsvps.json")
        insert_user_data(user_data, cursor)
        insert_venue_data(venue_data, cursor)
        insert_event_data(event_data, cursor)
        insert_rsvp_data(rsvp_data, cursor)
        connection.commit()
    finally:
        cursor.close()
        connection.close()  
