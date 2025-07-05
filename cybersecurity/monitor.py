"""Service monitoring utilities."""

from __future__ import annotations

import os
import time
from urllib.parse import urlparse

import httpx

from utils.logger import log


# Default service URLs sourced from environment variables
VECTOR_STORE_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")


def check_service(url: str) -> bool:
    """Return ``True`` if an HTTP GET request to ``url`` succeeds."""
    try:
        response = httpx.get(url, timeout=5.0)
        return response.status_code < 500
    except Exception:
        return False


def _check_vector_store(url: str) -> bool:
    return check_service(url)


def _check_broker(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return check_service(url)

    if parsed.scheme == "redis":
        try:
            import redis  # optional dependency
        except Exception:
            return False
        try:
            client = redis.Redis(host=parsed.hostname, port=parsed.port or 6379, db=int(parsed.path.lstrip("/") or 0))
            client.ping()
            return True
        except Exception:
            return False

    return False


def check_services(vector_url: str | None = None, broker_url: str | None = None) -> None:
    """Run a single round of service checks and log failures."""
    v_url = vector_url or VECTOR_STORE_URL
    b_url = broker_url or BROKER_URL

    if not _check_vector_store(v_url):
        log(f"Vector store check failed for {v_url}")
    if not _check_broker(b_url):
        log(f"Message broker check failed for {b_url}")


def monitor_services(interval: int = 60) -> None:
    """Continuously monitor services at the given interval (seconds)."""
    while True:
        check_services()
        time.sleep(interval)
