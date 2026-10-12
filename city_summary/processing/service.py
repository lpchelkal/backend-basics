from clients.exceptions import *
from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import apply_preprocessing


def build_city_summary(city: str, currency: str = "USD") -> dict:
    weather = get_weather(city)
    rate = get_rate(currency)
    summary = {
        "city": city,
        "weather": {
            "temp_c": weather["temp_c"],
            "description": weather["description"],
        },
        "rates": {
            "currency": currency.upper(),
            "rate_to_rub": rate,
        },
    }
    return apply_preprocessing(summary, weather.get("code"))
