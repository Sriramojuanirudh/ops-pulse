from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="OpsPulse", version="0.1.0")


class ServiceSignal(BaseModel):
    service: str
    latency_ms: float
    error_rate: float
    throughput: int


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "service": "ops-pulse"}


@app.get("/metrics")
def metrics() -> Dict[str, Any]:
    return {
        "services": [
            {"name": "checkout-api", "latency_ms": 180, "error_rate": 0.05, "throughput": 1234},
            {"name": "payments-api", "latency_ms": 320, "error_rate": 0.12, "throughput": 980},
            {"name": "auth-service", "latency_ms": 140, "error_rate": 0.02, "throughput": 2100},
        ],
        "summary": {
            "healthy_services": 2,
            "warning_services": 1,
            "critical_services": 0,
        },
    }


@app.post("/analyze")
def analyze_signals(signals: List[ServiceSignal]) -> Dict[str, Any]:
    findings = []

    for signal in signals:
        if signal.error_rate > 0.1 or signal.latency_ms > 300:
            issue = "performance_degradation"
        elif signal.error_rate > 0.05:
            issue = "error_spike"
        else:
            issue = "healthy"

        findings.append({
            "service": signal.service,
            "status": issue,
            "recommendation": "Check upstream dependency health and recent deploys." if issue != "healthy" else "No action needed.",
        })

    return {"findings": findings}


@app.get("/alerts")
def alerts() -> List[Dict[str, str]]:
    return [
        {"id": "ALERT-101", "service": "payments-api", "severity": "high", "message": "Latency spike detected"},
        {"id": "ALERT-102", "service": "checkout-api", "severity": "medium", "message": "Elevated error rate"},
    ]
