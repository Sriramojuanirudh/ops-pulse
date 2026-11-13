from __future__ import annotations

import json
from typing import Any, Dict, List
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(
    title="OpsPulse",
    version="1.1.0",
    description="AI-powered observability and incident intelligence platform.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ServiceSignal(BaseModel):
    service: str
    latency_ms: float
    error_rate: float
    throughput: int


SERVICE_DATA = [
    {"name": "checkout-api", "latency_ms": 182, "error_rate": 0.04, "throughput": 1250, "region": "us-east-1"},
    {"name": "payments-api", "latency_ms": 335, "error_rate": 0.14, "throughput": 980, "region": "us-west-2"},
    {"name": "auth-service", "latency_ms": 141, "error_rate": 0.02, "throughput": 2150, "region": "eu-west-1"},
    {"name": "inventory-service", "latency_ms": 210, "error_rate": 0.06, "throughput": 1680, "region": "ap-south-1"},
]

ALERTS = [
    {"id": "ALERT-201", "service": "payments-api", "severity": "high", "message": "Latency spike detected on the payment pipeline."},
    {"id": "ALERT-202", "service": "checkout-api", "severity": "medium", "message": "Error rate above normal threshold for 7 minutes."},
    {"id": "ALERT-203", "service": "inventory-service", "severity": "low", "message": "Throughput dropped by 13% in the last interval."},
]

INCIDENTS = [
    {
        "id": "INC-1001",
        "service": "payments-api",
        "status": "Investigating",
        "summary": "Payment processing latency spike and elevated retry count after deployment.",
        "impact": "customer checkout degradation",
    },
    {
        "id": "INC-1002",
        "service": "checkout-api",
        "status": "Mitigated",
        "summary": "Partial service degradation caused by upstream dependency timeouts.",
        "impact": "slow storefront response",
    },
]

WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Severe thunderstorm",
}


def classify_signal(signal: Dict[str, Any]) -> str:
    if signal.get("error_rate", 0) > 0.1 or signal.get("latency_ms", 0) > 300:
        return "critical"
    if signal.get("error_rate", 0) > 0.05 or signal.get("latency_ms", 0) > 220:
        return "warning"
    return "healthy"


def _fetch_json(url: str) -> Dict[str, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "OpsPulse-Weather/1.0"})
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _weather_label(code: Any) -> str:
    return WEATHER_CODE_MAP.get(int(code), "Weather conditions")


def _build_forecast_payload(city: str) -> Dict[str, Any]:
    location_query = quote_plus(city.strip() or "New York")
    geocode_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={location_query}&count=1&language=en&format=json"
    )
    search_results = _fetch_json(geocode_url)
    if "results" not in search_results or not search_results["results"]:
        raise ValueError(f"No weather data found for '{city}'.")

    result = search_results["results"][0]
    latitude = result["latitude"]
    longitude = result["longitude"]
    timezone = result.get("timezone", "auto")

    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        f"&timezone={quote_plus(timezone)}&forecast_days=7"
    )

    forecast_data = _fetch_json(forecast_url)
    current = forecast_data.get("current", {})
    daily = forecast_data.get("daily", {})

    if not current:
        raise ValueError(f"Weather data unavailable for '{city}'.")

    daily_forecast = []
    for index, day in enumerate(daily.get("time", [])):
        daily_forecast.append(
            {
                "date": day,
                "high": daily.get("temperature_2m_max", [0])[index],
                "low": daily.get("temperature_2m_min", [0])[index],
                "condition": _weather_label(daily.get("weather_code", [0])[index]),
            }
        )

    return {
        "city": result.get("name", city),
        "country": result.get("country", ""),
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "condition": _weather_label(current.get("weather_code")),
        "daily": daily_forecast,
    }


@app.get("/")
async def landing_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_type": "landing",
            "services": SERVICE_DATA,
            "alerts": ALERTS,
            "incidents": INCIDENTS,
        },
    )


@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_type": "dashboard",
            "services": SERVICE_DATA,
            "alerts": ALERTS,
            "incidents": INCIDENTS,
        },
    )


@app.get("/weather")
async def weather_dashboard(request: Request):
    return templates.TemplateResponse(
        "weather.html",
        {
            "request": request,
            "default_city": "San Francisco",
        },
    )


@app.get("/api/weather")
async def get_weather(city: str = "San Francisco") -> Dict[str, Any]:
    try:
        return _build_forecast_payload(city)
    except Exception as exc:  # pragma: no cover - defensive path
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "service": "ops-pulse"}


@app.get("/metrics")
def metrics() -> Dict[str, Any]:
    service_metrics = []
    healthy_count = 0
    warning_count = 0
    critical_count = 0

    for service in SERVICE_DATA:
        state = classify_signal(service)
        if state == "healthy":
            healthy_count += 1
        elif state == "warning":
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
                "status": state,
            }
        )

    return {
        "services": service_metrics,
        "summary": {
            "healthy_services": healthy_count,
            "warning_services": warning_count,
            "critical_services": critical_count,
        },
    }


@app.get("/alerts")
def get_alerts() -> List[Dict[str, str]]:
    return ALERTS


@app.get("/incidents")
def get_incidents() -> List[Dict[str, str]]:
    return INCIDENTS


@app.post("/analyze")
def analyze_signals(signals: List[ServiceSignal]) -> Dict[str, Any]:
    findings = []
    for signal in signals:
        status = classify_signal(
            {
                "latency_ms": signal.latency_ms,
                "error_rate": signal.error_rate,
                "throughput": signal.throughput,
            }
        )

        if status == "critical":
            recommendation = "Investigate recent deployment and dependency timeouts immediately."
        elif status == "warning":
            recommendation = "Monitor upstream dependency health and compare against recent baseline trends."
        else:
            recommendation = "No action required; service remains within baseline thresholds."

        findings.append(
            {
                "service": signal.service,
                "status": status,
                "recommendation": recommendation,
            }
        )

    return {"findings": findings}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
