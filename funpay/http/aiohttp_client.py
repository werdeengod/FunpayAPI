from typing import Literal

import aiohttp

from funpay.http.exceptions import HttpRequestError
from .base_client import BaseClient


class AioHttpClient(BaseClient[aiohttp.ClientSession]):
    def get_session(self) -> 'aiohttp.ClientSession':
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                base_url=self.BASE_URL
            )

        return self.session

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def request(self, method: Literal['GET', 'POST'], url: str, **kwargs) -> aiohttp.ClientResponse:
        session = self.get_session()

        response = await session.request(
            method=method,
            url=url,
            headers=self._get_headers(method),
            **kwargs
        )

        if response.status >= 400:
            raise HttpRequestError

        return response

    async def load_users_page_html(self, account_id: int) -> str:
        response = await self.request(
            method="GET",
            url=f'/users/{account_id}/'
        )

        return await response.text()

    async def load_lots_trade_page_html(self, node_id: int) -> str:
        response = await self.request(
            method="GET",
            url=f'/lots/{node_id}/trade'
        )

        return await response.text()
