from typing import TYPE_CHECKING, Optional

import aiohttp
from fake_useragent import FakeUserAgent
from aiocache import cached

from funpay.session import AiohttpSession
from funpay.exceptions import APIErrorFactory

if TYPE_CHECKING:
    from funpay.session import SessionABC


class Requester:
    def __init__(self, golden_key: str, session: Optional['SessionABC'] = None):
        if not session:
            self.session = AiohttpSession()
        else:
            self.session = session

        self.golden_key = golden_key

    def _get_headers(self, method: str = "GET") -> dict:
        base_headers = {
            "User-Agent": FakeUserAgent().random,
            "Cookie": f"golden_key={self.golden_key}",
            "Accept": "application/json, text/html",
            "Connection": "keep-alive"
        }

        if method.upper() == "POST":
            base_headers.update({
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": self.session.BASE_URL,
                "Referer": f"{self.session.BASE_URL}/"
            })

        return base_headers

    @cached(ttl=5)
    async def __call__(self, *, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        session = self.session.get()
        response = await session.request(method, url, headers=self._get_headers(method), **kwargs)

        if response.status >= 400:
            raise APIErrorFactory(response.status)

        return response
