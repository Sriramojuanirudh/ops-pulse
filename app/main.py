from __future__ import annotations

import json
from typing import Any, Dict, List
from urllib.parse import quote_plus
from urllib.request import Request as URLRequest, urlopen

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
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
    0: "Clear sky", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Heavy drizzle", 56: "Freezing drizzle", 57: "Heavy freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 77: "Snow grains", 80: "Rain showers",
    81: "Heavy rain showers", 82: "Violent rain showers", 85: "Snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Severe thunderstorm",
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
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min"
        "&hourly=temperature_2m,precipitation_probability,weather_code"
        f"&timezone={quote_plus(timezone)}&forecast_days=7&forecast_hours=24"
    )
    data = _fetch_json(url)
    current, daily, hourly = data.get("current", {}), data.get("daily", {}), data.get("hourly", {})
    if not current:
        raise ValueError(f"Weather data unavailable for '{city}'.")
    daily_forecast = [
        {"date": day, "high": daily["temperature_2m_max"][i], "low": daily["temperature_2m_min"][i], "condition": _weather_label(daily["weather_code"][i])}
        for i, day in enumerate(daily.get("time", []))
    ]
    hourly_forecast = []
    for i, timestamp in enumerate(hourly.get("time", [])):
        if timestamp < current.get("time", ""):
            continue
        hourly_forecast.append({
            "time": timestamp,
            "temperature": hourly["temperature_2m"][i],
            "precipitation_probability": hourly["precipitation_probability"][i],
            "condition": _weather_label(hourly["weather_code"][i]),
        })
        if len(hourly_forecast) == 12:
            break
    return {
        "city": city, "country": country, "latitude": latitude, "longitude": longitude, "timezone": timezone,
        "temperature": current.get("temperature_2m"), "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"), "wind_speed": current.get("wind_speed_10m"),
        "condition": _weather_label(current.get("weather_code")), "daily": daily_forecast, "hourly": hourly_forecast,
    }


def _build_forecast_payload(city: str) -> Dict[str, Any]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote_plus(city.strip())}&count=1&language=en&format=json"
    results = _fetch_json(url).get("results", [])
    if not results:
        raise ValueError(f"No weather data found for '{city}'.")
    place = results[0]
    return _forecast_at(place["latitude"], place["longitude"], place.get("name", city), place.get("country", ""), place.get("timezone", "auto"))


@app.middleware("http")
async def add_home_weather_preview(request: Request, call_next):
    response = await call_next(request)
    if request.url.path != "/" or "text/html" not in response.headers.get("content-type", ""):
        return response
    body = getattr(response, "body", None)
    if body is None:
        return response
    widget = r'''<style>
#home-weather-preview{position:fixed;right:22px;bottom:22px;z-index:1000;width:min(310px,calc(100vw - 32px));padding:16px 18px;border:1px solid rgba(148,188,255,.25);border-radius:16px;background:rgba(13,27,42,.96);color:#edf4ff;font:14px Inter,Arial,sans-serif;box-shadow:0 16px 46px rgba(0,0,0,.32);backdrop-filter:blur(12px)}
#home-weather-preview .hw-top{display:flex;justify-content:space-between;align-items:center;color:#a9d0ff;font-size:10px;font-weight:700;letter-spacing:1.2px}
#home-weather-preview .hw-live{color:#75efb2}#home-weather-preview .hw-main{display:flex;align-items:center;gap:12px;margin:12px 0 8px}#home-weather-preview .hw-temp{font-size:38px;font-weight:700;letter-spacing:-2px}#home-weather-preview .hw-desc{color:#c5d7f9}#home-weather-preview .hw-foot{display:flex;justify-content:space-between;align-items:center;color:#aebfe0;font-size:12px}#home-weather-preview a{color:#fff;text-decoration:none;background:linear-gradient(135deg,#3ea8ff,#685df2);padding:8px 11px;border-radius:9px;font-weight:600}#home-weather-preview a:hover{filter:brightness(1.12)}
@media(max-width:600px){#home-weather-preview{right:12px;bottom:12px}}
</style>
<aside id="home-weather-preview" aria-label="Local weather preview"><div class="hw-top"><span>LOCAL WEATHER</span><span class="hw-live">● LIVE</span></div><div class="hw-main"><span class="hw-temp" id="hw-temp">—°</span><span class="hw-desc"><strong id="hw-city">San Francisco</strong><br><span id="hw-condition">Loading forecast…</span></span></div><div class="hw-foot"><span id="hw-extra">A quick forecast at a glance</span><a href="/weather">Open weather →</a></div></aside>
<script>
(async()=>{try{const r=await fetch('/api/weather?city=San%20Francisco');if(!r.ok)throw new Error('Weather unavailable');const d=await r.json();document.getElementById('hw-temp').textContent=Math.round(d.temperature)+'°';document.getElementById('hw-city').textContent=d.city;document.getElementById('hw-condition').textContent=d.condition;document.getElementById('hw-extra').textContent='Feels like '+Math.round(d.feels_like)+'° · Humidity '+Math.round(d.humidity)+'%'}catch(_e){document.getElementById('hw-condition').textContent='See the latest forecast';document.getElementById('hw-extra').textContent='Weather details are one click away'}})();
</script>'''
    html = body.decode("utf-8", errors="replace")
    if "</body>" not in html.lower():
        return response
    import re
    updated = re.sub(r"</body\s*>", widget + "</body>", html, count=1, flags=re.IGNORECASE)
    headers = {k: v for k, v in response.headers.items() if k.lower() not in {"content-length", "content-encoding"}}
    return Response(content=updated, status_code=response.status_code, headers=headers, media_type="text/html")


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
            return _forecast_at(latitude, longitude, "Your location")
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
    counts = {"healthy": 0, "warning": 0, "critical": 0}
    services = []
    for service in SERVICE_DATA:
        state = classify_signal(service)
        counts[state] += 1
        services.append({**service, "status": state})
    return {"services": services, "summary": {"healthy_services": counts["healthy"], "warning_services": counts["warning"], "critical_services": counts["critical"]}}


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
