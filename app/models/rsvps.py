from db.connection import get_connection

def create_rsvp(user_id, event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rsvps (attendee_id, event_id) VALUES (%s, %s) RETURNING *",
        (user_id, event_id)
    )
    conn.commit()
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    rsvp = dict(zip(columns, row))
    return rsvp