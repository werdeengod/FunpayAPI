from typing import TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar('T')


class SessionABC(ABC, Generic[T]):
    BASE_URL: str = 'https://funpay.com'

    def __init__(self):
        self.session = None

    @abstractmethod
    def get(self) -> T:
        pass

    @abstractmethod
    async def close(self):
        pass
