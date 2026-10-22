import sqlite3
from pathlib import Path
from typing import Any, Dict, List

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ops_pulse.db"


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db() -> None:
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                summary TEXT NOT NULL,
                status TEXT NOT NULL,
                impact TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL
            )
            """
        )

        if conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO incidents (service, summary, status, impact) VALUES (?, ?, ?, ?)",
                (
                    "payments-api",
                    "Payment processing latency spike and elevated retry count after deployment.",
                    "Investigating",
                    "customer checkout degradation",
                ),
            )
            conn.execute(
                "INSERT INTO incidents (service, summary, status, impact) VALUES (?, ?, ?, ?)",
                (
                    "checkout-api",
                    "Partial service degradation caused by upstream dependency timeouts.",
                    "Mitigated",
                    "slow storefront response",
                ),
            )

        if conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO alerts (service, severity, message) VALUES (?, ?, ?)",
                ("payments-api", "high", "Latency spike detected on the payment pipeline."),
            )
            conn.execute(
                "INSERT INTO alerts (service, severity, message) VALUES (?, ?, ?)",
                ("checkout-api", "medium", "Error rate above normal threshold for 7 minutes."),
            )
            conn.execute(
                "INSERT INTO alerts (service, severity, message) VALUES (?, ?, ?)",
                ("inventory-service", "low", "Throughput dropped by 13% in the last interval."),
            )

        conn.commit()


def _classify_service(service_data: Dict[str, Any]) -> str:
    if service_data.get("error_rate", 0) > 0.1 or service_data.get("latency_ms", 0) > 300:
        return "critical"
    if service_data.get("error_rate", 0) > 0.05 or service_data.get("latency_ms", 0) > 220:
        return "warning"
    return "healthy"


def get_dashboard_snapshot() -> Dict[str, Any]:
    services = [
        {"name": "checkout-api", "latency_ms": 182, "error_rate": 0.04, "throughput": 1250, "region": "us-east-1"},
        {"name": "payments-api", "latency_ms": 335, "error_rate": 0.14, "throughput": 980, "region": "us-west-2"},
        {"name": "auth-service", "latency_ms": 141, "error_rate": 0.02, "throughput": 2150, "region": "eu-west-1"},
        {"name": "inventory-service", "latency_ms": 210, "error_rate": 0.06, "throughput": 1680, "region": "ap-south-1"},
    ]

    service_metrics = []
    healthy_count = 0
    warning_count = 0
    critical_count = 0

    for service in services:
        status = _classify_service(service)
        if status == "healthy":
            healthy_count += 1
        elif status == "warning":
            warning_count += 1
        else:
            critical_count += 1

        service_metrics.append(
            {
                "name": service["name"],
                "latency_ms": service["latency_ms"],
                "error_rate": service["error_rate"],
                "throughput": service["throughput"],
                "region": service["region"],
                "status": status,
            }
        )

    with _get_connection() as conn:
        incidents = [
            {
                "id": f"INC-{row['id']}",
                "service": row["service"],
                "status": row["status"],
                "summary": row["summary"],
                "impact": row["impact"],
            }
            for row in conn.execute(
                "SELECT * FROM incidents ORDER BY id DESC LIMIT 10"
            ).fetchall()
        ]

        alerts = [
            {
                "id": f"ALERT-{row['id']}",
                "service": row["service"],
                "severity": row["severity"],
                "message": row["message"],
            }
            for row in conn.execute(
                "SELECT * FROM alerts ORDER BY id DESC LIMIT 10"
            ).fetchall()
        ]

    return {
        "services": service_metrics,
        "summary": {
            "healthy_services": healthy_count,
            "warning_services": warning_count,
            "critical_services": critical_count,
        },
        "alerts": alerts,
        "incidents": incidents,
    }


def save_incident(service: str, summary: str, status: str, impact: str) -> Dict[str, Any]:
    with _get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO incidents (service, summary, status, impact) VALUES (?, ?, ?, ?)",
            (service, summary, status, impact),
        )
        conn.commit()
        return {"id": f"INC-{cursor.lastrowid}"}


if __name__ == "__main__":
    initialize_db()
    print(f"Database initialized at {DB_PATH}")
