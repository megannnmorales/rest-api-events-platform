from db.connection import get_connection

def get_organiser_stats(organiser_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE id = %s", (organiser_id,))
    user = cursor.fetchone()
    cursor.execute("""
        SELECT COUNT(rsvps.id)
        FROM events
        LEFT JOIN rsvps ON rsvps.event_id = events.id
        WHERE events.organiser_id = %s
        GROUP BY events.id
    """, (organiser_id,))
    rsvp_counts = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*) FROM events GROUP BY organiser_id")
    
    all_totals = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()

    if user is None or len(rsvp_counts) == 0:
        return None

    total_events = len(rsvp_counts)
    rank = 1
    for total in all_totals:
        if total > total_events:
            rank += 1

    return {
        "organiser_id": organiser_id,
        "name": user[0],
        "total_events": total_events,
        "avg_attendance": round(sum(rsvp_counts) / total_events, 1),
        "best_attended_count": max(rsvp_counts),
        "organiser_rank": rank
    }