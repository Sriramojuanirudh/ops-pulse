from __future__ import annotations

import json
from typing import Any, Dict, List
from urllib.parse import quote_plus
from urllib.request import Request as URLRequest, urlopen

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
    {"id": "INC-1001", "service": "payments-api", "status": "Investigating", "summary": "Payment processing latency spike and elevated retry count after deployment.", "impact": "customer checkout degradation"},
    {"id": "INC-1002", "service": "checkout-api", "status": "Mitigated", "summary": "Partial service degradation caused by upstream dependency timeouts.", "impact": "slow storefront response"},
]

WEATHER_CODE_MAP = {
    0: "Clear sky", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Heavy drizzle", 56: "Freezing drizzle", 57: "Heavy freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain",
    67: "Heavy freezing rain", 71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains", 80: "Rain showers", 81: "Heavy rain showers", 82: "Violent rain showers",
    85: "Snow showers", 86: "Heavy snow showers", 95: "Thunderstorm",
    96: "Thunderstorm with hail", 99: "Severe thunderstorm",
}


def classify_signal(signal: Dict[str, Any]) -> str:
    if signal.get("error_rate", 0) > 0.1 or signal.get("latency_ms", 0) > 300:
        return "critical"
    if signal.get("error_rate", 0) > 0.05 or signal.get("latency_ms", 0) > 220:
        return "warning"
    return "healthy"


def _fetch_json(url: str) -> Dict[str, Any]:
    request = URLRequest(url, headers={"Accept": "application/json", "User-Agent": "OpsPulse-Weather/1.0"})
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _weather_label(code: Any) -> str:
    return WEATHER_CODE_MAP.get(int(code), "Weather conditions")


def _forecast_at(latitude: float, longitude: float, city: str, country: str = "", timezone: str = "auto") -> Dict[str, Any]:
    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        "&hourly=temperature_2m,precipitation_probability,weather_code"
        f"&timezone={quote_plus(timezone)}&forecast_days=7&forecast_hours=24"
    )
    forecast_data = _fetch_json(forecast_url)
    current = forecast_data.get("current", {})
    daily = forecast_data.get("daily", {})
    hourly = forecast_data.get("hourly", {})
    if not current:
        raise ValueError(f"Weather data unavailable for '{city}'.")

    daily_forecast = []
    for index, day in enumerate(daily.get("time", [])):
        daily_forecast.append({
            "date": day,
            "high": daily.get("temperature_2m_max", [])[index],
            "low": daily.get("temperature_2m_min", [])[index],
            "condition": _weather_label(daily.get("weather_code", [])[index]),
        })

    hourly_forecast = []
    for index, timestamp in enumerate(hourly.get("time", [])):
        if timestamp < current.get("time", ""):
            continue
        hourly_forecast.append({
            "time": timestamp,
            "temperature": hourly.get("temperature_2m", [])[index],
            "precipitation_probability": hourly.get("precipitation_probability", [])[index],
            "condition": _weather_label(hourly.get("weather_code", [])[index]),
        })
        if len(hourly_forecast) == 12:
            break

    return {
        "city": city,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "condition": _weather_label(current.get("weather_code")),
        "daily": daily_forecast,
        "hourly": hourly_forecast,
    }


def _build_forecast_payload(city: str) -> Dict[str, Any]:
    query = quote_plus(city.strip())
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&language=en&format=json"
    search_results = _fetch_json(geocode_url)
    results = search_results.get("results", [])
    if not results:
        raise ValueError(f"No weather data found for '{city}'.")
    result = results[0]
    return _forecast_at(
        result["latitude"], result["longitude"], result.get("name", city),
        result.get("country", ""), result.get("timezone", "auto"),
    )


def _build_forecast_for_coordinates(latitude: float, longitude: float) -> Dict[str, Any]:
    return _forecast_at(latitude, longitude, "Your location")


@app.get("/")
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "page_type": "landing", "services": SERVICE_DATA, "alerts": ALERTS, "incidents": INCIDENTS})


@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "page_type": "dashboard", "services": SERVICE_DATA, "alerts": ALERTS, "incidents": INCIDENTS})


@app.get("/weather")
async def weather_dashboard(request: Request):
    return templates.TemplateResponse("weather.html", {"request": request, "default_city": "San Francisco"})


@app.get("/api/weather")
def get_weather(city: str = "San Francisco", latitude: float | None = None, longitude: float | None = None) -> Dict[str, Any]:
    try:
        if latitude is not None and longitude is not None:
            return _build_forecast_for_coordinates(latitude, longitude)
        if latitude is not None or longitude is not None:
            raise ValueError("Both latitude and longitude are required.")
        if not city.strip():
            raise ValueError("Enter a city name to search.")
        return _build_forecast_payload(city)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "service": "ops-pulse"}


@app.get("/metrics")
def metrics() -> Dict[str, Any]:
    service_metrics = []
    counts = {"healthy": 0, "warning": 0, "critical": 0}
    for service in SERVICE_DATA:
        state = classify_signal(service)
        counts[state] += 1
        service_metrics.append({**service, "status": state})
    return {"services": service_metrics, "summary": {"healthy_services": counts["healthy"], "warning_services": counts["warning"], "critical_services": counts["critical"]}}


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
        status = classify_signal({"latency_ms": signal.latency_ms, "error_rate": signal.error_rate, "throughput": signal.throughput})
        recommendation = (
            "Investigate recent deployment and dependency timeouts immediately." if status == "critical"
            else "Monitor upstream dependency health and compare against recent baseline trends." if status == "warning"
            else "No action required; service remains within baseline thresholds."
        )
        findings.append({"service": signal.service, "status": status, "recommendation": recommendation})
    return {"findings": findings}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
