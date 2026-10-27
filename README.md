# Rest API Events Platform

This API allows users to register, browse events, RSVP, and manage their attendance. Organisers can create and manage events, and view statistics about their audience.

## Technologies

- Python 3.13.15
- psql (17.11)

## Setup

1. Fork and clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
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
```

**`.env.test`**
```
PGDATABASE=test_nc_plus_one
```

## Seeding the Development Database

```bash
ENV=development python -m db.seed
```

## Running the Tests

Tests use the test database, which is reset with fresh data from `db/data/test/` before every test. The tests set `ENV=test` automatically.

```bash
pytest
```