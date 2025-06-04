from enum import StrEnum


class Locale(StrEnum):
    RU = "ru"
    EN = "en"


class ResponseType(StrEnum):
    JSON = "json"
    TEXT = "text"