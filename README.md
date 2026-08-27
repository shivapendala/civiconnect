# CivicConnect - Enterprise Smart City & Municipal Grievance Platform

CivicConnect is an enterprise-grade, multi-tenant municipal management and citizen engagement platform. It empowers city councils, administrative wards, and municipal departments to streamline grievance intake, automate AI triage, enforce SLA compliance, optimize field worker dispatch, and monitor urban IoT telemetry in real-time.

---

## 🏛️ System Architecture

```
                                  [ Citizen Mobile App ] (Flutter / Dart)
                                  [ Citizen Web Portal ] (React / TypeScript)
                                             │
                                             ▼
                                  [ NGINX Reverse Proxy ]
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
        [ Django / Channels Core API ]                  [ FastAPI Vision / NLP ]
        - Multi-tenancy & RBAC                          - Hazard Detection (YOLO)
        - SLA Escalation Engine                         - NLP Triage & Urgency
        - GIS Geofencing & Heatmaps                     - Duplicate Resolution
        - Field Workforce Dispatch                      - Audio Transcription
                      │                                             │
                      └──────────────────────┬──────────────────────┘
                                             ▼
                                [ PostgreSQL + Redis ]
                                [ Celery Async Pool  ]
```

---

## 📦 Prerequisites & Dependencies

- **Python**: >= 3.10
- **Node.js**: >= 18.x with `npm`
- **Docker & Docker Compose**: >= 24.x
- **Flutter SDK**: >= 3.19.x (for mobile application)
- **PostgreSQL**: >= 15.x
- **Redis**: >= 7.x

---

## ⚙️ Installation

### 1. Clone & Set Up Environment Variables
```bash
# Copy example environment configuration
cp example.env .env
```

### 2. Install Backend & AI Dependencies
```bash
# Python Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install Python requirements
pip install -r backend/requirements.txt
pip install -r ai-service/requirements.txt
```

### 3. Install Web Admin Portal Dependencies
```bash
cd web
npm install
cd ..
```

---

## 🔨 Build Instructions

To build all frontend bundles and compile backend bytecode:
```bash
# Build React Admin Portal
npm run build --prefix web

# Compile Python Services
python -m compileall backend ai-service
```

Alternatively, use the project `Makefile`:
```bash
make build
```

---

## 🚀 Run Instructions

### Option A: Docker Compose (Recommended)
Launch the complete multi-container stack including PostgreSQL, Redis, Django API, FastAPI Vision, and React Portal:
```bash
docker-compose up --build -d
```

### Option B: Local Microservices Execution
```bash
# 1. Database Migrations
python backend/manage.py migrate

# 2. Run Backend API Server (Port 8000)
python backend/manage.py runserver 0.0.0.0:8000

# 3. Run AI Vision Microservice (Port 8001)
uvicorn ai-service.main:app --host 0.0.0.0 --port 8001 --reload

# 4. Run React Web Portal (Port 3000)
npm run dev --prefix web
```

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/token/` | JWT Authentication & Token Issuance |
| `GET` | `/api/v1/complaints/` | List and filter civic grievances with spatial indexing |
| `POST` | `/api/v1/complaints/` | Create grievance with auto SLA calculation |
| `POST` | `/api/v1/complaints/{id}/transition/` | State machine lifecycle status transition |
| `GET` | `/api/v1/gis/heatmap/` | Weighted density heatmap points for GIS rendering |
| `POST` | `/api/v1/ai/triage/` | AI-assisted category and priority scoring |
| `POST` | `/api/v1/iot/ingest/` | Real-time smart sensor telemetry stream ingestion |
| `GET` | `/api/v1/analytics/kpis/` | Executive municipal KPI metrics & SLA compliance |

---

## 🔒 Security & Privacy

- **Data Isolation**: Complete multi-tenant schema isolation per municipal tenant.
- **PII Anonymization**: Automated masking of citizen phone numbers, emails, and exact coordinates on public feeds.
- **Cryptographic Audit Logs**: Immutable audit trail for all staff actions and administrative transitions.
- **Zero Committed Secrets**: Strict `.gitignore` policy enforcing non-sensitive environment configuration.
