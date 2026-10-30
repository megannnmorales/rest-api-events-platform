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

