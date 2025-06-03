from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from funpay.enums import Locale
    import datetime


@dataclass(frozen=True)
class Account:
    id: int
    csrf_token: str
    username: str
    locale: 'Locale'
    balance: Optional[int] = None

    def __str__(self):
        return self.username


@dataclass(frozen=True)
class Lot:
    id: int
    node: 'Node'
    title: str
    price: float
    amount: Optional[int] = None

    def __str__(self):
        return self.title


@dataclass(frozen=True)
class RaiseNode:
    node: 'Node'
    message: str
    success: bool


@dataclass(frozen=True)
class Node:
    id: int
    name: str


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
    date: 'datetime.datetime'

    def __str__(self) -> str:
        return self.content


@dataclass(frozen=True)
class Chat:
    id: int
    interlocutor_id: str
    messages: list['Message']
