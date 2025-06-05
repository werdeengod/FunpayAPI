from enum import StrEnum, IntEnum


class Locale(StrEnum):
    RU = "ru"
    EN = "en"


class ResponseType(StrEnum):
    JSON = "json"
    TEXT = "text"


class StatusOrder(IntEnum):
    PAID = 0
    CLOSED = 1
    REFUNDED = 2


class OrderType(IntEnum):
    PURCHASE = 0
    SALE = 1
