from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    COMPLETED = "completed"


class DrinkSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Order(BaseModel):
    id: int = Field(gt=0)
    drink: str = Field(min_length=1, max_length=100)
    size: DrinkSize
    quantity: int = Field(gt=0)
    customer_name: str | None = Field(default=None, min_length=1, max_length=100)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime


class OrderCreate(BaseModel):
    drink: str = Field(
        min_length=1,
        max_length=100,
        description="Название напитка из меню",
        examples=["Латте"],
    )
    size: DrinkSize = Field(
        description="Размер порции: small/medium/large",
        examples=[DrinkSize.MEDIUM],
    )
    quantity: int = Field(
        gt=0,
        description="Количество порций",
        examples=[2],
    )
    customer_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Имя клиента (необязательно)",
        examples=["клиент1"],
    )


class OrderUpdate(BaseModel):
    drink: str | None = Field(default=None, min_length=1, max_length=100)
    size: DrinkSize | None = None
    quantity: int | None = Field(default=None, gt=0)
    customer_name: str | None = Field(default=None, min_length=1, max_length=100)
    status: OrderStatus | None = None
