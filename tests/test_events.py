def test_get_events_responds_with200(client):
    response = client.get("/events")

    assert response.status_code == 200

def test_get_events_responds_with_list_on_key_of_events(client):
    events = client.get("/events").json()["events"]

    assert isinstance(events, list)


def test_check_returns_all_events(client):
    result = client.get("/events").json()["events"]
    expected = [
    {
        "id": 3,
        "title": "event_e",
        "description": "description_e",
        "starts_at": "2025-12-31T23:30:00+00:00",
        "ends_at": "2026-01-01T01:00:00+00:00",
        "organiser_id": 3,
        "venue_id": 1
    },
    {
        "id": 4,
        "title": "event_b",
        "description": "description_b",
        "starts_at": "2026-01-01T10:00:00+00:00",
        "ends_at": "2026-01-01T12:00:00+00:00",
        "organiser_id": 2,
        "venue_id": 1
    },
    {
        "id": 1,
        "title": "event_d",
        "description": "description_d",
        "starts_at": "2026-02-02T10:00:00+00:00",
        "ends_at": "2026-02-02T11:00:00+00:00",
        "organiser_id": 1,
        "venue_id": 3
    },
    {
        "id": 5,
        "title": "event_c",
        "description": "description_c",
        "starts_at": "2026-02-02T10:00:00+00:00",
        "ends_at": "2026-02-02T12:00:00+00:00",
        "organiser_id": 3,
        "venue_id": 2
    },
    {
        "id": 2,
        "title": "event_a",
        "description": "description_a",
        "starts_at": "2026-03-03T10:00:00+00:00",
        "ends_at": "2026-03-03T12:00:00+00:00",
        "organiser_id": 2,
        "venue_id": 3
    }
]
    assert result == expected

def test_get_events_returns_events(client):
    events = client.get("/events").json()["events"]

    assert len(events) == 5