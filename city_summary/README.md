# City summary

CLI-сводка по городу: погода (Open-Meteo, без ключа) + курс валюты к рублю (Frankfurter).

## Установка

```bash
cd city_summary
pip install -r requirements.txt
```

## Запуск

```bash
python main.py --city Moscow
python main.py --city Moscow --currency EUR
```

Валюта по умолчанию — `USD`.

## Пример вывода

```
Город: Moscow
Погода: 11.9°C, Overcast
Тёплая одежда: нет
USD→RUB: 84.84
Дорогой курс: нет
Зонт: нет
```

## Правила

- Температура < 0 → `warm_clothes: true`.
- Курс > 100 → `expensive: true`.
- Дождливый код погоды → зонт брать.

## Коды выхода

- `0` — успех.
- `2` — ошибка аргументов (нет `--city`).
- `3` — город или код валюты не найден.
- `4` — внешний сервис недоступен после повторов.

## Источники данных

- Погода: `https://geocoding-api.open-meteo.com` + `https://api.open-meteo.com` (только GET).
- Курсы: `https://api.frankfurter.dev/v2/rate/{currency}/RUB` (только GET).
