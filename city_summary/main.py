import argparse
import sys

from clients.exceptions import City_not_found, Currency_not_found, Server_unavailable
from processing.service import build_city_summary


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Сводка по городу: погода + курс валюты")
    parser.add_argument("--city", required=True, help="Название города")
    parser.add_argument("--currency", default="USD", help="ISO-код валюты (по умолчанию USD)")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2

    try:
        summary = build_city_summary(args.city, args.currency)
    except (City_not_found, Currency_not_found) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 3
    except Server_unavailable as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 4

    weather = summary["weather"]
    rates = summary["rates"]
    print(f"Город: {summary['city']}")
    print(f"Погода: {weather['temp_c']}°C, {weather['description']}")
    print(f"Тёплая одежда: {'да' if weather['warm_clothes'] else 'нет'}")
    print(f"{rates['currency']}→RUB: {rates['rate_to_rub']}")
    print(f"Дорогой курс: {'да' if rates['expensive'] else 'нет'}")
    if "umbrella" in weather:
        print(f"Зонт: {'да' if weather['umbrella'] else 'нет'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
