# Project Context — Jireh-Style Internal Dashboard

## Purpose
This project is being built as a portfolio piece to demonstrate Django + PostgreSQL skills
for a job application at Jireh Industries (Ardrossan, AB). The role is AI-Assisted Software
Developer, and the JD explicitly calls out Django, Wagtail, PostgreSQL, and Linux as the
existing stack for their public website. This project targets that gap directly.

The finished project should be deployed (Railway or Render, free tier) with a live URL,
and pushed to GitHub with a strong README explaining why it was built and what it demonstrates.

---

## Candidate Background
- Name: Jeremy Steem
- Current stack: Python, SQL (T-SQL/Oracle), React, JavaScript, Power BI, Power Automate
- AI tools in daily use: Claude Pro, Microsoft Copilot, Gemini Pro, GitHub Copilot
- Gaps this project addresses: Django, PostgreSQL, Linux (deployment), web-based internal tooling

---

## What We're Building
A small internal web application modeled on Jireh's stated internal tooling needs.
Three features:

1. **Asset/Equipment Tracker** — CRUD interface for assets (name, status, location, last updated).
   Maps to "develop tools for simplified interaction with ERP data."

2. **Task / Change Log** — Submit and track tasks/change requests with status
   (open, in progress, done). Filterable list view.
   Maps to "implement task and project tracking systems."

3. **Role-Based Access** — Two user roles (admin, viewer) using Django's built-in auth.
   Admins can create/edit; viewers are read-only.
   Maps to "apply role-based access controls for clarity and simplicity."

**Stack:** Django, PostgreSQL, HTML/CSS, minimal JS, deployed on Railway or Render.

---

## 4-Hour Build Plan

| Block | Time  | Goal                                                                 | Status      |
|-------|-------|----------------------------------------------------------------------|-------------|
| 1     | 45min | Environment setup: venv, Django, PostgreSQL, first runserver, Git   | DONE |
| 2     | 60min | Models + migrations: Asset and Task models, PostgreSQL connected     | DONE |
| 3     | 60min | Views + templates: list, detail, create form for both models         | DONE |
| 4     | 30min | Auth: login/logout, admin vs viewer groups, restrict write to admin  | DONE |
| 5     | 30min | Polish: index page, basic CSS, seed data                             | DONE |
| 6     | 15min | Deploy to Railway or Render, push to GitHub with README              | CONFIG DONE - awaiting GitHub push + hosting setup |

---

## Project Location
`C:\Users\Jeremy Steem\Desktop\Claude_Code\Django-PostgreSQL-Demo`

No work has been completed yet. Start at Block 1.

---

## Block 1 — Step-by-Step Instructions

### Prerequisites
Confirm in terminal before starting:
```bash
python --version    # Need 3.10+
pip --version
psql --version      # Need PostgreSQL installed
```

If PostgreSQL is not installed: https://www.postgresql.org/download/
During install: set a password for the postgres superuser, leave port at 5432.

---

### Step 1 — Virtual environment (5 min)
```bash
cd "C:\Users\Jeremy Steem\Desktop\Claude_Code\Django-PostgreSQL-Demo"
python -m venv venv
venv\Scripts\activate
```
Prompt should show `(venv)` when active.

---

### Step 2 — Install dependencies (5 min)
```bash
pip install django psycopg2-binary python-dotenv
```
Verify: `python -m django --version` — should show 5.x

---

### Step 3 — Create Django project and app (5 min)
```bash
django-admin startproject config .
python manage.py startapp dashboard
```

Expected structure:
```
Django-PostgreSQL-Demo/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dashboard/
│   ├── models.py
│   ├── views.py
│   └── ...
├── manage.py
└── venv/
```

---

### Step 4 — Create PostgreSQL database (5 min)
Open a separate terminal (not the venv one):
```bash
psql -U postgres
```
At the postgres=# prompt:
```sql
CREATE DATABASE jireh_dashboard;
CREATE USER jireh_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE jireh_dashboard TO jireh_user;
\q
```
Note the password — you'll need it in the next step.

---

### Step 5 — Create .env file (2 min)
Create `.env` in the project root:
```
DB_NAME=jireh_dashboard
DB_USER=jireh_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=replace-with-a-long-random-string
```
Generate a secret key with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### Step 6 — Update settings.py (10 min)
At the top of `config/settings.py`, add:
```python
from dotenv import load_dotenv
import os
load_dotenv()
```

Replace the SECRET_KEY line:
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key')
```

Replace the DATABASES block:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

Add `'dashboard'` to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'dashboard',
]
```

---

### Step 7 — Migrate and verify (5 min)
```bash
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000 — Django rocket ship = success.

---

### Step 8 — Initialize Git (5 min)
```bash
git init
```

Create `.gitignore` in project root:
```
venv/
__pycache__/
*.pyc
.env
db.sqlite3
```

First commit:
```bash
git add .
git commit -m "Initial Django + PostgreSQL setup"
```

---

## Block 2 Preview — Models & Migrations
Once Block 1 is complete, tell Claude Code:
"Block 1 is done. Move to Block 2 — define Asset and Task models in dashboard/models.py,
run migrations, and set up the Django admin for both models."

### Asset model fields to define:
- `name` (CharField)
- `status` (CharField with choices: active, inactive, maintenance)
- `location` (CharField)
- `notes` (TextField, optional)
- `last_updated` (DateTimeField, auto_now=True)
- `created_at` (DateTimeField, auto_now_add=True)

### Task model fields to define:
- `title` (CharField)
- `description` (TextField)
- `status` (CharField with choices: open, in_progress, done)
- `created_by` (ForeignKey to User)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

---

## Notes for Claude Code Sessions
- Always activate venv before running any manage.py commands: `venv\Scripts\activate`
- The .env file holds all secrets — never commit it
- When Block N is complete, update the status table at the top of this file
- Target: working live URL + GitHub repo with README before the application deadline (June 14, 2026)
