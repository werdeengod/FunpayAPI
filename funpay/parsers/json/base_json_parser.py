from typing import Any

from funpay.parsers import ABCParser


class BaseJsonParser(ABCParser):
    def __init__(self, data: dict | list):
        super().__init__(data)
        self.data = data

    def _parse_implementation(self, **kwargs) -> Any:
        raise NotImplementedError
    