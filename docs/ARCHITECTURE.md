# OpsPulse

OpsPulse is an AI-powered observability platform for distributed systems. It helps engineering teams detect anomalies earlier, correlate service signals, and understand incident impact faster.

## What it does

- Tracks service health across latency, error rate, and throughput
- Groups active alerts and incident summaries in a unified dashboard
- Classifies service health as healthy / warning / critical
- Exposes clean API endpoints for metrics and incident analysis
- Provides a startup-ready landing page and operational dashboard

## Tech stack

- Python 3.11
- FastAPI
- SQLite for local persistence
- Jinja2 templates
- Vanilla JavaScript frontend

## Project structure

- `app/main.py` — FastAPI application and request handlers
- `app/store.py` — SQLite storage and telemetry logic
- `templates/` — landing and dashboard HTML templates
- `static/` — CSS and JavaScript frontend assets
- `data/` — SQLite database storage

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- http://localhost:8000/
- http://localhost:8000/dashboard

## API overview

- `GET /api/health` — health check
- `GET /api/metrics` — service summary and incident snapshot
- `GET /api/incidents` — recent incidents
- `GET /api/alerts` — active alerts
- `POST /api/incidents` — create a new incident
- `POST /api/analyze` — analyze service telemetry payloads

## Docker

```bash
docker build -t ops-pulse .
docker run -p 8000:8000 ops-pulse
```

Or with Docker Compose:

```bash
docker-compose up --build
```

## Roadmap

- Add real OpenTelemetry ingestion
- Add dependency graph mapping
- Add AI incident summarization and recommendations
- Add auth, RBAC, and multi-team support
- Add persistent PostgreSQL and alert routing integrations
