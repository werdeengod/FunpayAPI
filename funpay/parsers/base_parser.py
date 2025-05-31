from typing import Any
from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self) -> Any:
        pass
