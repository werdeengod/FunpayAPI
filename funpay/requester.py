from typing import TYPE_CHECKING, Optional, Literal

import aiohttp
from fake_useragent import FakeUserAgent
from aiocache import cached

from funpay.session import BaseClientSession
from funpay.exceptions import APIErrorFactory

if TYPE_CHECKING:
    from funpay.session import SessionABC


class Requester:
    """HTTP request handler for FunPay API with authentication support.

    Handles authenticated requests to FunPay including:
    - Automatic header generation
    - Session management
    - Response error handling
    - Caching of frequent requests

    Args:
        golden_key (str): Authentication key from FunPay cookies
        session (Optional[SessionABC]): Custom session handler. If None,
            creates a default BaseClientSession.

    Attributes:
        golden_key (str): Stored authentication key
        session (SessionABC): HTTP session manager instance
    """
    def __init__(self, golden_key: str, session: Optional['SessionABC'] = None):
        if not session:
            self.session = BaseClientSession()
        else:
            self.session = session

        self.golden_key = golden_key

    def _get_headers(self, method: Literal["POST", "GET"]) -> dict:
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
    async def __call__(self, *, method: Literal["POST", "GET"], url: str, **kwargs) -> aiohttp.ClientResponse:
        """Execute authenticated HTTP request (main interface).

        Args:
            method: HTTP method ("GET" or "POST")
            url: Endpoint URL (relative to base)
            **kwargs: Additional arguments for aiohttp request

        Returns:
            aiohttp.ClientResponse: Response object

        Raises:
            APIError: For status codes >= 400 (via APIErrorFactory)

        Note:
            Responses are cached for 5 seconds (TTL) to prevent
            duplicate requests to the same endpoint.
        """
        session = self.session.get()
        response = await session.request(method, url, headers=self._get_headers(method), **kwargs)

        if response.status >= 400:
            raise APIErrorFactory(response.status)

        return response

    async def load_users_page(self, account_id: int) -> str:
        """Load HTML content of user profile page.

        Args:
            account_id: FunPay user ID to load

        Returns:
            str: Raw HTML content of the profile page

        Raises:
            APIError: If request fails (404, 403 etc.)
        """
        response = await self(
            method='GET',
            url=f'/users/{account_id}/'
        )

        html = await response.text()
        return html

    async def load_lots_page(self, node_id: str) -> str:
        """Load HTML content of lots trading page.

        Args:
            node_id: Category/node ID to load lots from

        Returns:
            str: Raw HTML content of the lots page

        Raises:
            APIError: If request fails
        """
        response = await self(
            method='GET',
            url=f'/lots/{node_id}/trade'
        )

        html = await response.text()
        return html

