from .exceptions import Currency_not_found, Server_unavailable
from .http import http_get

RATE_URL = "https://api.frankfurter.dev/v2/rate"


def get_rate(currency: str) -> float:
    code = currency.upper()
    data = http_get(f"{RATE_URL}/{code}/RUB")
    if not data.get("rate"):
        raise Currency_not_found(f"валюта не найдена: {code}")
    try:
        return float(data["rate"])
    except (KeyError, TypeError, ValueError):
        raise Server_unavailable("некорректный ответ")
