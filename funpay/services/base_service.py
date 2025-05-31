from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from funpay.exceptions import APIErrorFactory

if TYPE_CHECKING:
    from pydantic import BaseModel
    from funpay.models import Account
    from funpay.requester import Requester


class BaseService(ABC):
    def __init__(self, account: 'Account', requester: 'Requester'):
        if not account:
            raise APIErrorFactory(401, 'Unauthorized')

        self._account = account
        self._requester = requester

    @property
    def requester(self) -> 'Requester':
        return self._requester

    @property
    def account(self) -> 'Account':
        return self._account

    @abstractmethod
    async def get(self) -> 'BaseModel':
        pass

