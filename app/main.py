from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import random
import time
import logging

app = FastAPI()
log = logging.getLogger(__name__)

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["path", "status"]
)

@app.get("/health")
def health():
    http_requests_total.labels(path="/health", status="200").inc()
    return {"status": "ok"}

@app.get("/slow")
def slow(ms: int = 250):
    log.info(f"slow endpoint called ms={ms}")
    time.sleep(ms / 1000.0)
    http_requests_total.labels(path="/slow", status="200").inc()
    return {"slept_ms": ms}

@app.get("/error")
def error(rate: int = 50):
    """
    rate = procent szans na 500 (0-100)
    """
    roll = random.randint(1, 100)

    if roll <= rate:
        log.error(f"simulated error roll={roll} rate={rate}")
        http_requests_total.labels(path="/error", status="500").inc()
        return Response(
            content='{"detail":"simulated error"}',
            status_code=500,
            media_type="application/json"
        )

    log.info(f"request ok roll={roll} rate={rate}")
    http_requests_total.labels(path="/error", status="200").inc()
    return {"ok": True, "roll": roll, "rate": rate}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)