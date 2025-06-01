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
class RaiseNode:
    node_id: str
    message: str
    success: bool


@dataclass(frozen=True)
class Review:
    username: str
    order_code: str
    date: str
    text: str

    def __str__(self):
        return f"{self.username}: {self.text}"


@dataclass(frozen=True)
class Message:
    id: int
    chat_id: int
    content: str
    author_id: int

    def __str__(self) -> str:
        return self.content
