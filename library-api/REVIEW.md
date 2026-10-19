# Саморевью по чек-листу

Прошёл по пунктам чек-листа и сверил с `openapi.yaml`.

## Ресурсы и URL

- [x] Path — существительные во множественном числе, kebab-case: `/books`, `/readers`, `/loans`.
- [x] Глагольных URL нет, кроме осознанного действия `/loans/{id}/return`.
- [x] `id` конкретного ресурса — в path, фильтры — в query: `/loans/{id}`, `/loans?status=overdue`.
- [x] Версия API — в `servers`: `https://api.library.example.com/v1`.
- [x] CRUD для Books и Readers, у Loans — создание, список, чтение и возврат.

## Методы и коды

- [x] `POST` при создании отдаёт `201` и `Location`.
- [x] `DELETE` отдаёт `204` без тела.
- [x] Пустой список — это `200` и `items: []`, а не `404`.
- [x] Бизнес-конфликт — `409`, ошибка валидации — `422`, не найдено — `404`.

## Схемы

- [x] Отдельные схемы на чтение и запись: `Book` / `BookCreate` / `BookUpdate`, `Reader` / `ReaderCreate` / `ReaderUpdate`, `Loan` / `LoanCreate`.
- [x] `available_copies` есть только в `Book`, помечен `readOnly` и не попадает в request-схемы.
- [x] `additionalProperties: false` во всех request-схемах — лишнее поле не пройдёт.
- [x] `returned_at` допускает `null` (`type: [string, 'null']`).
- [x] Общие схемы подключены через `$ref`, руками не копируются.

## Ошибки и списки

- [x] Все ошибки — один `ErrorResponse`.
- [x] В enum все шесть кодов из задания.
- [x] Для 422 есть пример с `details` по конкретному полю.
- [x] У коллекций есть фильтры, сортировка и пагинация.
- [x] У `limit` есть `default` и `maximum`.
- [x] `GET /loans?status=overdue` описан, и понятно, что значит overdue.

## Идемпотентность и бизнес-правила

- [x] `Idempotency-Key` обязателен на `POST /loans`.
- [x] Описан полный replay: тот же `201`, то же тело, `Idempotent-Replay: true`.
- [x] Описан mismatch: тот же ключ с другим телом — `409 IDEMPOTENCY_MISMATCH`.
- [x] Описан конкурентный повтор: `409` + `Retry-After`.
- [x] Указан TTL — 24 часа.
- [x] Выдача только при `available_copies > 0` — `409`.
- [x] Не больше 5 активных выдач на читателя — `409`.
- [x] Возврат через `POST`, запись о выдаче остаётся.
- [x] Нельзя удалить книгу или читателя с активными выдачами — `409`.
- [x] `due_date` позже текущей даты — иначе `422`.

## Документация

- [x] Теги `Books`, `Readers`, `Loans` проставлены у всех операций.
- [x] У каждой операции есть `summary`, у ключевых — `description`.
- [x] Примеров больше трёх, есть и успешные ответы, и ошибки (`duplicateIsbn`, `noCopies`, `idempotencyMismatch`, `alreadyReturned`).

## Файлы

- [x] `openapi.yaml`
- [x] `STYLE.md`
- [x] `REVIEW.md`
- [x] `README.md`