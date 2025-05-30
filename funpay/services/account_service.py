from typing import TYPE_CHECKING

import aiohttp

from funpay.parser import AccountParser
from .base_service import BaseService

if TYPE_CHECKING:
    from funpay.models import Review, Lot


class AccountService(BaseService):
    async def _request(self) -> aiohttp.ClientResponse:
        response = await self._requester(
            method='get',
            url=f'/users/{self.account.id}/'
        )

        return response

    async def reviews(self) -> list['Review']:
        response = await self._request()
        html = await response.text()
        return AccountParser(html).reviews()

    async def lots(self) -> list['Lot']:
        response = await self._request()
        html = await response.text()
        return AccountParser(html).lots()
