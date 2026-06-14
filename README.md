# Jireh-Style Internal Dashboard

A small internal web application for tracking equipment/assets and tasks/change
requests, with role-based access control. Built as a portfolio piece to
demonstrate Django + PostgreSQL skills.

**Live demo:** https://django-postgresql-demo.onrender.com/

> Hosted on Render's free tier — the service spins down after periods of
> inactivity, so the first load after idling may take 30-60 seconds.

## Why this project exists

This project was built as a direct response to a job posting from Jireh
Industries (Ardrossan, AB) for an **AI-Assisted Software Developer**. The job
description calls out Django, Wagtail, PostgreSQL, and Linux as the stack
behind Jireh's public website, and lists internal tooling needs such as:

- "develop tools for simplified interaction with ERP data"
- "implement task and project tracking systems"
- "apply role-based access controls for clarity and simplicity"

This app demonstrates working knowledge of that exact stack by implementing a
small but complete version of each of those needs.

## Features

1. **Asset / Equipment Tracker** — list, detail, and create views for assets
   (name, status, location, notes, last updated).
2. **Task / Change Log** — list (filterable by status), detail, and create
   views for tasks, with status tracking (open / in progress / done).
3. **Role-Based Access** — Django auth with two groups:
   - `admin` — full read/write access (create assets and tasks).
   - `viewer` — read-only access to lists and detail pages.
4. **Dashboard home page** — at-a-glance counts of assets and tasks by status.

## Stack

- Django 5.2
- PostgreSQL
- Plain HTML templates + a small custom CSS file (no frontend framework)
- Gunicorn + WhiteNoise for production serving

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
DB_NAME=jireh_dashboard
DB_USER=jireh_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=replace-with-a-long-random-string
DEBUG=True
```

Create the PostgreSQL database and user:

```sql
CREATE DATABASE jireh_dashboard;
CREATE USER jireh_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE jireh_dashboard TO jireh_user;
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data   # optional sample data
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Roles

- Superusers and members of the `admin` group can create assets and tasks.
- Members of the `viewer` group (or anonymous visitors) can browse lists and
  detail pages but cannot create records.
- Groups are created automatically via migration (`admin`, `viewer`). Assign
  users to groups via `/admin/`.

## Deployment

The app is configured for Render or Railway:

- `requirements.txt` — pinned dependencies (includes `gunicorn`, `whitenoise`,
  `dj-database-url`).
- `Procfile` — runs migrations on release and serves with Gunicorn.
- `build.sh` — install deps, collect static files, run migrations.
- `runtime.txt` — Python version.
- Settings read `DATABASE_URL` (provided automatically by Render/Railway
  Postgres add-ons) or fall back to discrete `DB_*` env vars for local dev.
- Static files are served via WhiteNoise with compressed manifest storage.

### Required environment variables in production

```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
DATABASE_URL=...   # provided by the platform's Postgres add-on
```

## Project Structure

```
config/        # Django project settings, URLs, WSGI
dashboard/     # App: models (Asset, Task), views, templates, admin, seed data
```
