from typing import Optional

from funpay.requester import Requester
from funpay.services import AccountService, LotService
from funpay.parser import AccountParser
from funpay.exceptions import APIErrorFactory


class FunpayAPI:
    def __init__(self, golden_key: str, *, requester: Optional[Requester] = None):
        self.golden_key = golden_key

        self._requester = requester if requester else Requester(golden_key)
        self._account = None

    async def __aenter__(self) -> 'FunpayAPI':
        return await self.login()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._requester.session.close()

    @property
    def account_service(self) -> 'AccountService':
        if not self._account:
            raise APIErrorFactory(401, 'Unauthorized')

        return AccountService(self._account, self._requester)

    @property
    def lot_service(self) -> 'LotService':
        if not self._account:
            raise APIErrorFactory(401, 'Unauthorized')

        return LotService(self._account, self._requester)

    async def login(self) -> 'FunpayAPI':
        response = await self._requester(
            method='get',
            url='/'
        )

        html = await response.text()
        self._account = AccountParser(html).get()
        return self
