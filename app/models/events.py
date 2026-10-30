from db.connection import get_connection


def list_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT id, title, description, starts_at, ends_at, organiser_id, venue_id 
    FROM events 
    ORDER BY starts_at ASC, id ASC;""")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    events = [dict(zip(columns, row)) for row in rows]
    return events


def get_one_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, venues.address, venues.capacity, events.created_at 
    FROM events
    JOIN venues ON events.venue_id = venues.id 
    WHERE events.id = %s""", (event_id,))
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    cursor.close()
    conn.close()
    event = dict(zip(columns, row))
    return event

def create_event(title, description, starts_at, ends_at, venue_id, organiser_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
        (title, description, starts_at, ends_at, organiser_id, venue_id)
    )
    conn.commit()
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    event = dict(zip(columns, row))
    return event