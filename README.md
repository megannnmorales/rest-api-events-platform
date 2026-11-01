# Rest API Events Platform

This API allows users to register, browse events, RSVP, and manage their attendance. Organisers can create and manage events, and view statistics about their audience.

## Technologies

- Python 3.13
- FastAPI
- PostgreSQL (psql 17.11) with psycopg2 (raw SQL, no ORM)
- pytest

## Setup

1. Fork and clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

Create the development and test databases:

```bash
psql -d postgres -f db/setup_db.sql
```

## Environment Variables

Create two files in the root of the project. They are listed in `.gitignore`, so you must create them yourself after cloning.

**`.env.development`**
```
PGDATABASE=nc_plus_one
SECRET_KEY=<a random string of at least 32 characters>
```

**`.env.test`**
```
PGDATABASE=test_nc_plus_one
SECRET_KEY=<a random string of at least 32 characters>
```

## Seeding the Development Database

```bash
ENV=development python -m db.seed
```

## Running the API

```bash
ENV=development uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Authentication

1. Register with `POST /api/auth/register`.
2. Log in with `POST /api/auth/login` to receive an access token.
3. Send the token with requests to protected endpoints:
   ```
   Authorization: Bearer <token>
   ```

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/auth/register` | Register a new user | No |
| POST | `/api/auth/login` | Log in and receive a token | No |
| GET | `/api/events` | List all events | No |
| GET | `/api/events/{event_id}` | Get a single event | No |
| POST | `/api/events` | Create an event | Yes |
| PATCH | `/api/events/{event_id}` | Update an event (organiser only) | Yes |
| POST | `/api/events/{event_id}/rsvp` | RSVP to an event | Yes |
| GET | `/api/events/{event_id}/attendees` | List an event's attendees (organiser only) | Yes |
| GET | `/api/user/me/events` | List events you have RSVPed to | Yes |
| GET | `/api/organisers/{organiser_id}/stats` | Get an organiser's statistics | No |

## Error Format

All errors return the same shape:

```json
{
  "error": {
    "code": "Not Found",
    "message": "Event not found",
    "details": null
  }
}
```

## Running the Tests

Tests use the test database, which is reset with fresh data from `db/data/test/` before every test. The tests set `ENV=test` automatically.

```bash
pytest
```