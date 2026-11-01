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

def get_event_organiser(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT events.organiser_id
    FROM events
    WHERE events.id = %s""", (event_id,))
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    cursor.close()
    conn.close()
    event_organiser = dict(zip(columns, row))
    return event_organiser

def create_event(title, description, starts_at, ends_at, venue_id, organiser_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
        (title, description, starts_at, ends_at, organiser_id, venue_id)
    )
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    event = dict(zip(columns, row))
    return event

def change_event(event_id, description=None, starts_at=None, ends_at=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE events 
    SET description = COALESCE(%s, description), 
        starts_at = COALESCE(%s, starts_at), 
        ends_at = COALESCE(%s, ends_at) 
    WHERE id = %s 
    RETURNING *""",
    (description, starts_at, ends_at, event_id)
    )
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    conn.commit()
    cursor.close()
    conn.close()
    event = dict(zip(columns, row))
    return event


def list_attendees(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT rsvps.attendee_id AS id, users.name, users.email
    FROM rsvps
    JOIN users ON rsvps.attendee_id = users.id
    WHERE rsvps.event_id = %s""", (event_id,))
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    attendees = [dict(zip(columns, row)) for row in rows]
    return attendees