# OpsPulse Architecture

## Overview

OpsPulse is an AI-assisted observability platform for engineering teams. It ingests service telemetry, detects anomalies, correlates events, and surfaces likely root cause explanations.

## System design

### 1. Frontend dashboard
- HTML/CSS/JavaScript-generated dashboard
- Displays service health, alerts, and incidents
- Serves as a lightweight product experience for MVP validation

### 2. API layer
- FastAPI service exposes endpoints for:
  - health checks
  - metrics summaries
  - active alerts
  - incident reporting
  - anomaly analysis

### 3. Telemetry model
- Service signals include:
  - service name
  - latency in milliseconds
  - error rate
  - throughput
  - region

### 4. Intelligence layer
- Rule-based detection for alerts
- Correlation logic across service signals
- AI-ready architecture for future LLM-powered incident summarization

### 5. Storage and extension
- Current MVP uses in-memory data for fast prototyping
- Future versions can integrate with:
  - PostgreSQL
  - Redis
  - Timeseries databases
  - Kafka or event brokers
  - OpenTelemetry collectors

## Data flow

1. Services emit telemetry.
2. API receives metrics and signal snapshots.
3. App classifies service health.
4. Matching rules create alerts and incident summaries.
5. Dashboard renders operational state to engineering users.

## Future architecture

- OpenTelemetry collector for logs, metrics, and traces
- Event ingestion service
- AI summarization model for incident narratives
- Notification layer for Slack and email
- Authentication and RBAC for team access
- Cloud deployment templates for Kubernetes, Render, or AWS

## Why this architecture fits the product

This design is intentionally simple for an MVP while keeping a clear path toward enterprise-scale production systems.
