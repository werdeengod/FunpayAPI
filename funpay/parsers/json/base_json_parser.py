from typing import Any

from funpay.parsers import ABCParser


class BaseJsonParser(ABCParser):
    def __init__(self, data: dict | list):
        super().__init__()
        self.data = data

    def parse(self) -> Any:
        raise NotImplementedError
    