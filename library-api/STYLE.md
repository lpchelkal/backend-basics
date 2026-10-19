# API Style Guide (Library API)

1. **URL — существительные во множественном числе, kebab-case.** `/books`, `/readers`, `/loans`.

2. **JSON — snake_case** `book_id`, `due_date`, `available_copies`.

3. **Серверные поля — readOnly.** `id`, `available_copies`, `registered_at`, `loaned_at`, `returned_at` клиент не передаёт.

4. **Один формат ошибок.** Всегда `ErrorResponse { code, message, details? }`, где `code` — из фиксированного enum: `INVALID_REQUEST`, `NOT_FOUND`, `VALIDATION_ERROR`, `CONFLICT`, `BUSINESS_RULE_VIOLATION`, `IDEMPOTENCY_MISMATCH`.

5. **Коды ответов по смыслу.** 200 — чтение и обновление, 201 — создание, 204 — удаление, 400 — битый запрос, 404 — не найдено, 409 — конфликт или бизнес-правило, 422 — ошибка валидации полей.

6. **Коллекции — пагинация, фильтры и сортировка.** `page` (с 1) и `limit` (1–100, по умолчанию 20), фильтры отдельными query-параметрами, сортировка `sort=<field>:<dir>`, ответ: `{ items, page, limit, total }`.

7. **Создание выдачи идемпотентно.** `POST /loans` требует `Idempotency-Key`.
