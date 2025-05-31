from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    id: int
    csrf_token: str
    username: str
    balance: Optional[int] = None

    def __str__(self):
        return self.username


@dataclass(frozen=True)
class Lot:
    node_id: int
    title: str
    price: float
    amount: Optional[int] = None

    def __str__(self):
        return self.title


@dataclass(frozen=True)
class Review:
    username: str
    order_code: str
    date: str
    text: str

    def __str__(self):
        return f"{self.username}: {self.text}"
