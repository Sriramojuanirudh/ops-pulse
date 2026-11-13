# OpsPulse Architecture

## Overview

OpsPulse is an AI-assisted observability platform for engineering teams. It ingests service telemetry, detects anomalies, correlates events, and surfaces likely root cause explanations.

## System design

### 1. Frontend
- Landing page for product pitch and positioning
- Dashboard for service health, incidents, and alerts
- Lightweight JavaScript rendering for dynamic overview cards

### 2. API layer
- FastAPI endpoints for health checks, service telemetry, and incident actions
- Clean separation between presentation and logic

### 3. Storage layer
- SQLite for local development and demo data persistence
- Seeded telemetry and incident records for product validation

### 4. Intelligence layer
- Rule-based classification for service health
- Alert severity evaluation based on latency and error thresholds
- Extension point for future AI summarization and anomaly detection

### 5. Deployment
- Docker support for containerized development and deployment
- Compose-based local environment for quick iteration

## Data flow

1. Service metrics are sent to the API.
2. Telemetry is analyzed and classified.
3. Alerts and incidents are generated or persisted.
4. Dashboard renders status, trends, and actionable insights.

## Future roadmap

- OpenTelemetry collectors for real metrics and traces
- PostgreSQL for production-ready persistence
- AI summarization and inferred root-cause analysis
- Slack/email notifications and incident routing
- RBAC, audit logs, and enterprise team management
