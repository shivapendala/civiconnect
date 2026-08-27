# CivicConnect

## Overview

CivicConnect is a full‑stack platform for municipal complaint management, citizen engagement, and city analytics. It consists of:

- **Backend** – Django REST Framework APIs, Celery workers, AI services (RAG, vision), JWT authentication, RBAC, audit logging, rate limiting, secure file handling.
- **Frontend** – Flutter mobile/web app with offline‑first sync, gamification, dashboards, and admin UI.
- **DevOps** – Docker‑compose multi‑service stack (PostgreSQL, Redis, Nginx, Celery, AI service).

## Getting Started

### Prerequisites

- Python 3.11+ and `pip`
- Docker Desktop (or Docker Engine + Compose)
- Flutter 3.13+ (for web/mobile development)
- Node 20+ (optional for CI scripts)

### Installation

```bash
# Clone the repo
git clone https://github.com/shivapendala/civiconnect.git
cd civiconnect

# Backend setup (virtualenv recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# Apply migrations & create a superuser
python manage.py migrate
python manage.py createsuperuser

# Install Flutter dependencies
cd mobile
flutter pub get
```

### Running locally

```bash
# From the project root start all services
docker compose up -d --build

# Backend API (available at http://localhost:8000/api/)
# Flutter web (available at http://localhost)
```

### Testing

```bash
# Backend tests
pytest backend/
# Flutter widget tests
flutter test
```

## Architecture

- **Django** – core data models (`Complaint`, `Category`, `Department`, `User`), REST API, Celery tasks for background processing.
- **AI Services** – mock Vision and RAG pipelines; ready to swap for real models.
- **Flutter** – offline sync manager, connectivity listener, gamification UI, analytics dashboard.
- **Security** – JWT auth, RBAC permissions, input validation, CSRF protection, rate limiting, secure headers.

## License

Proprietary – all rights reserved.
