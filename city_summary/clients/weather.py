from .exceptions import City_not_found, Server_unavailable
from .http import http_get

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODE_DESC = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    97: "Heavy thunderstorm",
    99: "Thunderstorm with heavy hail",
}


def text_description(desc_code) -> str:
    return WEATHER_CODE_DESC.get(desc_code, "Unknown")


def get_weather(city: str) -> dict:
    geo = http_get(GEO_URL, {"name": city, "count": 1})
    if not geo.get("results"):
        raise City_not_found(f"город не найден: {city}")
    try:
        lat = float(geo["results"][0]["latitude"])
        lon = float(geo["results"][0]["longitude"])
    except (KeyError, TypeError, ValueError):
        raise Server_unavailable("некорректный ответ сервера")

    forecast = http_get(
        FORECAST_URL,
        {"latitude": lat, "longitude": lon, "current": "temperature_2m,weather_code"},
    )
    if not forecast.get("current"):
        raise Server_unavailable("некорректный ответ прогноза")
    try:
        temp = float(forecast["current"]["temperature_2m"])
    except (KeyError, TypeError, ValueError):
        raise Server_unavailable("некорректный ответ прогноза")
    code = forecast["current"].get("weather_code")
    return {"temp_c": temp, "description": text_description(code), "code": code}
