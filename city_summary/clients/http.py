import time

import requests

from .exceptions import Server_unavailable

MAX_ATTEMPTS = 3
TIMEOUT = (3, 10)
RETRIABLE_5XX = (500, 502, 503, 504)


def http_get(url: str, params: dict | None = None) -> dict:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt == MAX_ATTEMPTS:
                raise Server_unavailable(f"недоступен: {url}")
            time.sleep(1)
            continue

        if response.status_code == 429:
            if attempt == MAX_ATTEMPTS:
                raise Server_unavailable(f"недоступен : {url}")
            raw = response.headers.get("Retry-After", "1")
            delay = int(raw) if raw.strip().isdigit() else 1
            time.sleep(delay)
            continue

        if response.status_code in RETRIABLE_5XX:
            if attempt == MAX_ATTEMPTS:
                raise Server_unavailable(f"недоступен : {url}")
            time.sleep(1)
            continue

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise Server_unavailable(f"некорректный json: {url}")
        return data

    raise Server_unavailable(f"недоступен: {url}")
