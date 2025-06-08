from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from funpay.enums import Locale, StatusOrder, OrderType
    import datetime


@dataclass(frozen=True)
class UserCut:
    id: Optional[int]
    username: Optional[str]

    def __str__(self):
        return self.username


@dataclass(frozen=True)
class User(UserCut):
    created_date: 'datetime.datetime'
    banned: bool
    last_online: Optional['datetime.datetime']


@dataclass(frozen=True)
class Account(UserCut):
    csrf_token: str
    locale: 'Locale'
    balance: Optional[int] = None


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
class Game:
    id: int
    name: str
    nodes: list['Node']


@dataclass(frozen=True)
class Review:
    user: 'UserCut'
    order_code: str
    date: str
    text: str

    def __str__(self):
        return f"{self.user}: {self.text}"


@dataclass(frozen=True)
class Message:
    id: int
    chat_id: int
    content: str
    author: 'UserCut'
    date: 'datetime.datetime'

    def __str__(self) -> str:
        return self.content


@dataclass(frozen=True)
class Chat:
    id: int
    interlocutor_id: str
    messages: list['Message']


@dataclass(frozen=True)
class ChatCut:
    id: int
    interlocutor_id: str
    last_message: 'Message'


@dataclass(frozen=True)
class OrderCut:
    id: str
    title: str
    status: 'StatusOrder'
    price: float
    start_date: 'datetime.datetime'
    order_type: Optional['OrderType']
    user: 'UserCut'


@dataclass(frozen=True)
class Order(OrderCut):
    end_date: 'datetime.datetime'
    description: str
    node: 'Node'

