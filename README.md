# Jireh-Style Internal Dashboard

A small internal web application for tracking equipment/assets and tasks/change
requests, with role-based access control. Built as a portfolio piece to
demonstrate Django + PostgreSQL skills.

**Live demo:** https://django-postgresql-demo.onrender.com/
**Source code:** https://github.com/JeremySteem/Django-PostgreSQL-Demo

> Hosted on Render's free tier — the service spins down after periods of
> inactivity, so the first load after idling may take 30-60 seconds.

---

## Table of Contents

1. [Why This Project Exists](#why-this-project-exists)
2. [About the Author](#about-the-author)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Project Tour (with Screenshots)](#project-tour-with-screenshots)
6. [Roles & Permissions](#roles--permissions)
7. [Project Structure](#project-structure)
8. [Local Setup](#local-setup)
9. [Deployment](#deployment)

---

## Why This Project Exists

This project was built as a direct response to a job posting from **Jireh
Industries** (Ardrossan, AB) for an **AI-Assisted Software Developer**. The
job description calls out Django, Wagtail, PostgreSQL, and Linux as the stack
behind Jireh's public website, and lists internal tooling needs such as:

- "develop tools for simplified interaction with ERP data"
- "implement task and project tracking systems"
- "apply role-based access controls for clarity and simplicity"

This app demonstrates working knowledge of that exact stack by implementing a
small but complete version of each of those needs — built and shipped
end-to-end (environment setup → models → views/templates → auth → polish →
deployment) in a single focused session.

## About the Author

- **Name:** Jeremy Steem
- **Current stack:** Python, SQL (T-SQL/Oracle), React, JavaScript, Power BI,
  Power Automate
- **AI tools in daily use:** Claude Pro, Microsoft Copilot, Gemini Pro, GitHub
  Copilot
- **Gaps this project addresses:** Django, PostgreSQL, Linux-style deployment,
  and web-based internal tooling — directly demonstrating the stack Jireh
  Industries uses for internal tools.

## Features

1. **Asset / Equipment Tracker** — list, detail, and create views for assets
   (name, status, location, notes, last updated). Maps to *"develop tools for
   simplified interaction with ERP data."*
2. **Task / Change Log** — list (filterable by status), detail, and create
   views for tasks, with status tracking (open / in progress / done). Maps to
   *"implement task and project tracking systems."*
3. **Role-Based Access** — Django auth with two groups:
   - `admin` — full read/write access (create assets and tasks).
   - `viewer` — read-only access to lists and detail pages.

   Maps to *"apply role-based access controls for clarity and simplicity."*
4. **Dashboard home page** — at-a-glance counts of assets and tasks by status.

## Tech Stack

- **Backend:** Django 5.2
- **Database:** PostgreSQL
- **Frontend:** Plain HTML templates + a small custom CSS file (no frontend
  framework)
- **Production serving:** Gunicorn + WhiteNoise (static files)
- **Hosting:** Render (free tier), deployed via `build.sh` + `Procfile`

---

## Project Tour (with Screenshots)

### 1. Logging In

Anonymous visitors can browse the site, but creating or editing records
requires logging in as an **admin** (or superuser).

![Login page](screenshots/Login.PNG)

Enter your username and password and click **Log In**. Once logged in, your
username appears in the top navigation bar along with a **Log Out** button.

### 2. Dashboard Home

After logging in, the home page gives an at-a-glance summary of the system:
total assets, and tasks broken down by status (Open, In Progress, Done).

![Dashboard home](screenshots/Dashboard.PNG)

From here you can jump straight to **View Assets** or **View Tasks**.

### 3. Assets

**Asset List** — every piece of equipment being tracked, with current status
and location. Click any asset name to view its full details. Admins see a
**+ New Asset** button.

![Assets list](screenshots/Assets.PNG)

**Asset Detail** — full record, including notes and timestamps.

![Single asset detail](screenshots/Single-Asset.PNG)

**Adding a New Asset** — fill in name, status (Active / Inactive /
Maintenance), location, and notes, then click **Save**.

![New asset form](screenshots/New-Asset.PNG)

**Updating an Asset** — edited via the Django admin panel under
**Admin → Dashboard → Assets**.

![Update asset in admin](screenshots/Update-Assets.PNG)

### 4. Tasks

**Task List** — all tracked tasks/change requests, with status, creator, and
date. Filterable by status via the dropdown.

![Tasks list](screenshots/Tasks.PNG)

**Task Detail** — full description, status, creator, and timestamps.

![Single task detail](screenshots/Single-Task.PNG)

**Adding a New Task** — enter a title, description, and initial status, then
click **Save**. The task is automatically attributed to the logged-in user.

![New task form](screenshots/New-Task.PNG)

**Updating a Task** — edited via the Django admin panel under
**Admin → Dashboard → Tasks**.

![Update task in admin](screenshots/Update-Tasks.PNG)

### 5. Admin Panel — Managing Users and Roles

The Django admin panel (`/admin/`) is where superusers manage accounts, roles,
and raw data.

![Admin home](screenshots/Admin.PNG)

**Managing Users** — under **Authentication and Authorization → Users**, add
new users, reset passwords, or change permissions.

![Users list](screenshots/Users.PNG)

To create a new user, click **Add User**, choose a username and password,
then assign them to a group.

![Add user form](screenshots/New-User.PNG)

**Managing Groups (Roles)** — under **Authentication and Authorization →
Groups**:

- **admin** — can create and edit Assets and Tasks.
- **viewer** — read-only access to Asset and Task lists/details.

![Groups list](screenshots/Groups.PNG)

To create a custom group with specific permissions, click **Add Group**, name
it, and choose permissions from the available list.

![New group form](screenshots/New-Group.PNG)

**Changing Your Password** — any logged-in user can change their own password
from the admin panel via the **Change Password** link in the top-right corner.

![Change password](screenshots/Change-Pass.PNG)

---

## Roles & Permissions

| Role | Can View | Can Create/Edit |
|------|----------|------------------|
| Anonymous | Asset & Task lists/details | — |
| Viewer | Asset & Task lists/details | — |
| Admin / Superuser | Everything | Assets, Tasks, and (if superuser) Users/Groups via Admin panel |

- Superusers and members of the `admin` group can create assets and tasks.
- Members of the `viewer` group (or anonymous visitors) can browse lists and
  detail pages but cannot create records.
- Groups (`admin`, `viewer`) are created automatically via migration. Assign
  users to groups via `/admin/`.

## Project Structure

```
config/        # Django project settings, URLs, WSGI
dashboard/     # App: models (Asset, Task), views, templates, admin, seed data
```

---

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
