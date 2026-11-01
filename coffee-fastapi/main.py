from datetime import datetime
from itertools import count
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response
from models import Order, OrderCreate, OrderStatus, OrderUpdate
from settings import Settings, get_settings

app = FastAPI(
    title="Учёт заказов кофейни",
    description="Сервис учёта заказов коффе",
    version="1.0.0",
)

SettingsDep = Annotated[Settings, Depends(get_settings)]
orders: dict[int, Order] = {}
next_id = count(1)


@app.get("/", tags=["сервис"], summary="приветствие от сервиса")
def hello(settings: SettingsDep):
    return {"message": f"hello from {settings.app_name}"}


@app.get("/info", tags=["сервис"], summary="информация о сервисе")
def info(settings: SettingsDep):
    return {
        "app_name": settings.app_name,
        "orders_count": len(orders),
    }


@app.post("/orders", status_code=201, response_model=Order, tags=["заказы"], summary="добавление заказа")
def create_order(order: OrderCreate):
    data = order.model_dump()
    data["id"] = next(next_id)
    data["created_at"] = datetime.now()
    new_order = Order(**data)
    orders[new_order.id] = new_order
    return new_order


@app.get("/orders/{order_id}", status_code=200, response_model=Order, tags=["заказы"], summary="получить заказ по id")
def get_order_by_id(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="заказ не найден")
    return orders[order_id]


@app.get("/orders", status_code=200, response_model=list[Order], tags=["заказы"], summary="получить список заказов")
def get_orders(
    settings: SettingsDep,
    status: OrderStatus | None = None,
    limit: int | None = None,
    offset: int = 0,
):
    page_size = settings.default_page_size if limit is None else limit
    page_size = min(page_size, settings.max_page_size)
    result = list(orders.values())
    if status is not None:
        result = [order for order in result if order.status == status]
    return result[offset : offset + page_size]


@app.patch("/orders/{order_id}", status_code=200, response_model=Order, tags=["заказы"], summary="обновление заказа")
def update_order(order_id: int, patch: OrderUpdate):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="заказ не найден")
    updated = orders[order_id].model_copy(update=patch.model_dump(exclude_unset=True))
    orders[order_id] = updated
    return updated


@app.delete("/orders/{order_id}", status_code=204, tags=["заказы"], summary="отмена заказа")
def delete_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="заказ не найден")
    del orders[order_id]
    return Response(status_code=204)
