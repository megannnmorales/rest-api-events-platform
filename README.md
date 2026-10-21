# Rest API Events Platform

This API allows users to register, browse events, RSVP, and manage their attendance. Organisers are able to create and manage events, and view statistics about their audience.


# Technologies
Python 3.13.15
psql (17.11)

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

# Database Setup

1. Run setup.sql file:
```bash
psql -d postgres -f db/setup.sql
```