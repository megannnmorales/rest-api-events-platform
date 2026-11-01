from db.connection import get_connection

def create_user(name, email, hashed_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, hashed_password) VALUES (%s, %s, %s) RETURNING *",
        (name, email, hashed_password)
    )
    conn.commit()
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    user = dict(zip(columns, row))
    return user

# def get_user_without_password(user_id):
#     conn = get_connection()
    
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
    
#     columns = [desc[0] for desc in cursor.description]
#     row = cursor.fetchone()
#     if row is None:
#             return None
#     cursor.close()
#     conn.close()
#     user = dict(zip(columns, row))

def get_user_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    cursor.close()
    conn.close()
    user = dict(zip(columns, row))

    return user


def list_user_rsvps(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT events.id, events.title, events.starts_at,
           rsvps.created_at AS rsvp_date,
           ROW_NUMBER() OVER (ORDER BY events.starts_at ASC) AS event_rank,
           COUNT(*) OVER () AS total_rsvps
        FROM rsvps
        JOIN events ON rsvps.event_id = events.id
        WHERE rsvps.attendee_id = %s
        ORDER BY events.starts_at ASC
    """, (user_id,))
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    attendees = [dict(zip(columns, row)) for row in rows]
    return attendees