from db.connection import get_connection

def get_user(email):

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