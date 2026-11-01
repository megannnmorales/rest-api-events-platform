from starlette.testclient import TestClient
import jwt
from datetime import datetime, timezone, timedelta
from utils.config import get_secret, ALGORITHM

# --- GET /api/events ---
def test_get_events_responds_with200(client: TestClient):
    response = client.get("/api/events")

    assert response.status_code == 200

def test_get_events_responds_with_list_on_key_of_events(client: TestClient):
    events = client.get("/api/events").json()["events"]

    assert isinstance(events, list)


def test_check_returns_all_events(client: TestClient):
    result = client.get("/api/events").json()["events"]
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

def test_get_events_returns_events(client: TestClient):
    events = client.get("/api/events").json()["events"]

    assert len(events) == 5

# --- GET /api/events/:id ---
def test_get_events_returns_specific_event(client):
    response = client.get("/api/events/1")
    assert response.status_code == 200
    assert response.json()["event"]["id"] == 1

def test_get_event_not_found_returns_404(client):
    response = client.get("/api/events/99999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

def test_get_event_not_valid_returns_400(client):
    response = client.get("/api/events/hi")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

# --- POST /api/events/:id/rsvp ---

def test_rsvp_created_with_valid_token(client, auth_headers):
    response = client.post("/api/events/1/rsvp",headers=auth_headers)
    
    assert response.status_code == 201
    body = response.json()
    rsvp = body["rsvp"]
    assert isinstance (rsvp,dict)
    assert rsvp["attendee_id"] == 2
    assert rsvp ["event_id"] == 1


def test_create_rsvp_with_missing_token_returns_401(client):
    response = client.post("/api/events/1/rsvp")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorized"

def test_create_rsvp_with_expired_token_returns_401(client):

    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) - timedelta(hours=1)
    }
    token = jwt.encode(payload, get_secret(), algorithm=ALGORITHM)

    response = client.post(
        "/api/events/1/rsvp",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401


def test_rsvp_to_missing_event_responds_with_404(client, auth_headers):
    response = client.post("/api/events/9999/rsvp", headers=auth_headers)

    assert response.status_code == 404

def test_duplicate_rsvp_responds_with_409(client, auth_headers):
    client.post("/api/events/1/rsvp", headers=auth_headers) 

    response = client.post("/api/events/1/rsvp", headers=auth_headers) 

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "Conflict"

# --- DELETE /api/events/:id/rsvp/me ---
def test_successfully_cancelled_rsvp_responds_with_204(client, auth_headers):
    client.post("/api/events/1/rsvp", headers=auth_headers)
    
    response = client.delete("api/events/1/rsvp/me", headers=auth_headers)

    assert response.status_code == 204

def test_without_a_valid_token_returns_401(client):
    response = client.delete("api/events/1/rsvp/me")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorized"

def test_cancelling_a_non_existent_rsvp_returns_404(client, auth_headers):
    response = client.delete("api/events/1/rsvp/me", headers=auth_headers)

    assert response.status_code == 404

# --- POST /api/events ---

def test_create_event_with_valid_token(client, auth_headers):
    response = client.post("/api/events", json= {
  "title": "Summer Rooftop Social",
  "description": "An evening of networking and good vibes.",
  "starts_at": "2025-08-15T18:00:00Z",
  "ends_at": "2025-08-15T21:00:00Z",
  "venue_id": 2
}
 , headers=auth_headers)
    
    assert response.status_code == 201
    body = response.json()
    event = body["event"]
    assert isinstance (event,dict)
    assert event["organiser_id"] == 2
    assert event["id"] == 6

def test_create_event_with_missing_token_returns_401(client):
    response = client.post("/api/events")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorized"

def test_create_event_with_expired_token_returns_401(client):

    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) - timedelta(hours=1)
    }
    token = jwt.encode(payload, get_secret(), algorithm=ALGORITHM)

    response = client.post(
        "/api/events",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

def test_malformed_event_field_returns_400(client, auth_headers):
    response = client.post(
        "/api/events",
        json={
            "name": "Python Workshop",
            "description": "Learn Python",
            "date": "not-a-date"
        },
        headers=auth_headers
    )

    assert response.status_code == 400

def test_create_event_with_valid_iso_dates(client, auth_headers):
    response = client.post(
        "/api/events/",
        headers=auth_headers,
        json={
            "title": "Summer Rooftop Social",
            "description": "An evening of networking and good vibes.",
            "starts_at": "2026-11-15T18:00:00Z",
            "ends_at": "2026-11-15T21:00:00Z",
            "venue_id": 2
        }
    )

    assert response.status_code == 201

    event = response.json()["event"]

    assert datetime.fromisoformat(
    event["starts_at"].replace("Z", "+00:00")
    ) == datetime.fromisoformat("2026-11-15T18:00:00+00:00")

def test_create_event_with_invalid_dates(client, auth_headers):
    response = client.post(
    "/api/events/",
    headers=auth_headers,
    json={
        "title": "Summer Rooftop Social",
        "description": "An evening of networking and good vibes.",
        "starts_at": "not-a-date",
        "ends_at": "2026-11-15T21:00:00Z",
        "venue_id": 2
        }
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

# ---  PATCH/api/events ---
def test_change_event_is_successful(client, auth_headers):
    client.post(
        "/api/events/",
        headers=auth_headers,
        json={
            "title": "Summer Rooftop Social",
            "description": "An evening of networking and good vibes.",
            "starts_at": "2026-11-15T19:00:00Z",
            "ends_at": "2026-11-15T21:00:00Z",
            "venue_id": 2
            }
        )
    response = client.patch(
        "/api/events/6",
        headers=auth_headers,
        json={
            "description": "A morning of networking and good vibes.",
            "starts_at": "2026-11-15T11:00:00Z",
            "ends_at": "2026-11-15T12:00:00Z",
                }
            )
    assert response.status_code == 200
    assert response.json()["event"]["description"] == "A morning of networking and good vibes."


def test_change_event_is_successful_with_one_parameter(client, auth_headers):
    client.post(
        "/api/events/",
        headers=auth_headers,
        json={
            "title": "Summer Rooftop Social",
            "description": "An evening of networking and good vibes.",
            "starts_at": "2026-11-15T19:00:00Z",
            "ends_at": "2026-11-15T21:00:00Z",
            "venue_id": 2
            }
        )
    response = client.patch(
        "/api/events/6",
        headers=auth_headers,
        json={
            "description": "A morning of networking and good vibes.",
            "starts_at": "2026-11-15T19:00:00Z",
            "ends_at": "2026-11-15T21:00:00Z"
                }
            )
    assert response.status_code == 200
    assert response.json()["event"]["description"] == "A morning of networking and good vibes."


def test_change_event_ends_before_starts(client, auth_headers):
    response = client.patch(
        "/api/events/2",
        headers=auth_headers,
        json={
            "starts_at": "2026-11-15T21:00:00Z",
            "ends_at": "2026-11-15T18:00:00Z",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"


def test_change_event_ends_equal_to_starts(client, auth_headers):
    response = client.patch(
        "/api/events/2",
        headers=auth_headers,
        json={
            "starts_at": "2026-11-15T18:00:00Z",
            "ends_at": "2026-11-15T18:00:00Z",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_patch_event_only_ends_at_before_existing_start(client, auth_headers):
    response = client.patch(
        "/api/events/2",
        headers=auth_headers,
        json={"ends_at": "2000-01-01T00:00:00Z"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_change_event_not_organiser(client, other_auth_headers):
    response = client.patch(
        "/api/events/2",
        headers=other_auth_headers,
        json={"description": "Trying to change someone else's event"},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "Forbidden"

def test_change_event_not_found(client, auth_headers):
    response = client.patch(
        "/api/events/9999",
        headers=auth_headers,
        json={"description": "This event doesn't exist"},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"


def test_change_event_no_token(client):
    response = client.patch(
        "/api/events/1",
        json={"description": "No token sent"},
    )

    assert response.status_code == 401


def test_change_event_invalid_token(client):
    response = client.patch(
        "/api/events/1",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={"description": "Bad token sent"},
    )

    assert response.status_code == 401


# ---  GET/api/events/:id/attendees ---

def test_get_attendees_valid_event_and_user_returns_list_of_attendees(client, auth_headers):
    response = client.get("/api/events/2/attendees", headers=auth_headers)
    
    assert response.status_code == 200
    body = response.json()
    assert body["attendees"][0]["name"] == "user_b"
    assert body["attendees"][0]["email"] == "user_b@example.com"

def test_get_attendees_no_token(client):
    response = client.get("/api/events/2/attendees")

    assert response.status_code == 401


def test_get_attendees_invalid_token(client):
    response = client.get(
        "/api/events/2/attendees",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


def test_get_attendees_not_organiser(client, other_auth_headers):
    response = client.get("/api/events/2/attendees", headers=other_auth_headers)

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "Forbidden"


def test_get_attendees_no_password_in_response(client, auth_headers):
    response = client.get("/api/events/2/attendees", headers=auth_headers)

    assert response.status_code == 200
    for attendee in response.json()["attendees"]:
        assert "password" not in attendee


def test_get_attendees_event_not_found(client, auth_headers):
    response = client.get("/api/events/9999/attendees", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

# ---  GET /api/user/me/events ---

def test_get_my_events_success(client, auth_headers):
    response = client.get("/api/user/me/events", headers=auth_headers)
    print(response.json())
    assert response.status_code == 200
    events = response.json()["events"]
    assert events[0]["title"] == "event_e"


def test_get_my_events_ordered_by_starts_at_ascending(client, auth_headers):
    response = client.get("/api/user/me/events", headers=auth_headers)

    events = response.json()["events"]
    starts = [event["starts_at"] for event in events]
    assert starts == sorted(starts)


def test_get_my_events_event_rank_and_total_rsvps(client, auth_headers):
    response = client.get("/api/user/me/events", headers=auth_headers)

    events = response.json()["events"]
    assert events[0]["event_rank"] == 1
    assert events[0]["total_rsvps"] == len(events)


def test_get_my_events_no_token(client):
    response = client.get("/api/user/me/events")

    assert response.status_code == 401


def test_get_my_events_invalid_token(client):
    response = client.get(
        "/api/user/me/events",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


# --- GET organiser stats ---

def test_get_organiser_stats_success(client):
    response = client.get("/api/organisers/2/stats")

    assert response.status_code == 200, response.text
    stats = response.json()["stats"]
    assert stats["name"] == "user_a"


def test_get_organiser_stats_values_are_accurate(client):
    response = client.get("/api/organisers/2/stats")

    stats = response.json()["stats"]
  
    assert stats["organiser_id"] == 2
    assert stats["total_events"] == 2
    assert stats["avg_attendance"] == 0.5
    assert stats["best_attended_count"] == 1


def test_get_organiser_stats_avg_attendance_one_decimal(client):
    response = client.get("/api/organisers/1/stats")

    stats = response.json()["stats"]
    assert stats["avg_attendance"] == round(stats["avg_attendance"], 1)


def test_get_organiser_stats_rank(client):
    response = client.get("/api/organisers/1/stats")

    stats = response.json()["stats"]
    assert stats["organiser_rank"] == 3


def test_get_organiser_stats_organiser_not_found(client):
    response = client.get("/api/organisers/9999/stats")

    assert response.status_code == 404


def test_get_organiser_stats_organiser_has_no_events(client):
    response = client.get("/api/organisers/4/stats")

    assert response.status_code == 404