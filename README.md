# Online Course Assessment Project

This Django project was created to satisfy the assignment requirements for an
online course application with a new assessment feature.

## Setup

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py seed_demo_data
.\.venv\Scripts\python manage.py runserver
```

## Admin Login

- Username: `admin`
- Password: `Admin12345!`

## Useful URLs

- Course page: `http://127.0.0.1:8000/course/1/`
- Admin site: `http://127.0.0.1:8000/admin/`
