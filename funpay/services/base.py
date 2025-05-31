from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from funpay.types import Account
    from funpay.http import AioHttpClient


class BaseService:
    def __init__(self, account: 'Account', client: 'AioHttpClient'):
        self._account = account
        self._client = client

    @property
    def client(self) -> 'AioHttpClient':
        return self._client

    @property
    def account(self) -> 'Account':
        return self._account
