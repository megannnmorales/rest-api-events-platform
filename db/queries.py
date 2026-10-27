from db.connection import get_connection


def list_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, starts_at, ends_at, organiser_id, venue_id FROM events ORDER BY starts_at ASC, id ASC;")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    events = [dict(zip(columns, row)) for row in rows]
    return events