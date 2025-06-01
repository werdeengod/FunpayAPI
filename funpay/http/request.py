from typing import TYPE_CHECKING, Literal, TypeVar, Generic
import json

from fake_useragent import FakeUserAgent
from aiocache import cached

from funpay.http.exceptions import HttpRequestError

if TYPE_CHECKING:
    from funpay.http import BaseClient

T = TypeVar('T')


class Request(Generic[T]):
    """Generic HTTP request handler for making authenticated API calls.

    Provides methods for common requests with built-in session management,
    headers configuration, and error handling. Responses are typed using
    generic parameter T.

    Args:
        client: BaseClient instance providing session and authentication details
    """
    def __init__(self, client: 'BaseClient'):
        self.client = client

    def _get_headers(self, method: Literal["POST", "GET"]) -> dict:
        """Generate appropriate HTTP headers for the request method.

        Args:
            method: HTTP method ("POST" or "GET")

        Returns:
            Dictionary containing complete headers for the request
        """
        base_headers = {
            "User-Agent": FakeUserAgent().random,
            "Cookie": f"golden_key={self.client.golden_key}",
            "Accept": "application/json, text/html",
            "Connection": "keep-alive"
        }

        if method.upper() == "POST":
            base_headers.update({
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": self.client.BASE_URL,
                "Referer": f"{self.client.BASE_URL}/"
            })

        return base_headers

    @cached(ttl=10)
    async def _send_request(self, method: Literal["POST", "GET"], url: str, **kwargs: dict) -> T:
        """Low-level method to send HTTP requests with caching (10 second TTL).

        Args:
            method: HTTP method ("POST" or "GET")
            url: Endpoint URL (relative to client's BASE_URL)
            **kwargs: Additional arguments for the request

        Returns:
            Response object of type T

        Raises:
            HttpRequestError: If response status is 400 or higher
        """
        session = self.client.get_session()

        response = await session.request(
            method=method,
            url=url,
            headers=self._get_headers(method),
            **kwargs
        )

        if response.status >= 400:
            raise HttpRequestError(
                status=response.status,
                url=url,
                text=await response.text()
            )

        return response

    async def fetch_main_page(self) -> str:
        """Fetch the main page HTML content.

        Returns:
            Raw HTML content as string
        """
        response = await self._send_request(
            method='GET',
            url='/'
        )

        return await response.text()

    async def fetch_users_page(self, account_id: int) -> str:
        """Fetch user profile page HTML content.

        Args:
            account_id: Target user's account ID

        Returns:
            Raw HTML content as string
        """
        response = await self._send_request(
            method="GET",
            url=f'/users/{account_id}/'
        )

        return await response.text()

    async def fetch_lots_trade_page(self, node_id: int) -> str:
        """Fetch trading page HTML content for specific lot.

        Args:
            node_id: Trading node identifier

        Returns:
            Raw HTML content as string
        """
        response = await self._send_request(
            method="GET",
            url=f'/lots/{node_id}/trade'
        )

        return await response.text()

    async def send_raise(self, game_id: str, node_id: str) -> dict:
        """Submit a raise/up request for a trading lot.

        Args:
            game_id: Game session identifier
            node_id: Trading node identifier

        Returns:
            JSON response from server as dictionary
        """
        response = await self._send_request(
            method='POST',
            url='/lots/raise',
            data={
                "game_id": game_id,
                "node_id": node_id
            }
        )

        data = await response.json()
        return data

    async def send_message(self, chat_id: str | int, text: str, csrf_token: str) -> bool:
        """Send message to specified chat.

        Args:
            chat_id: Target chat identifier
            text: Message content
            csrf_token: CSRF protection token

        Returns:
            JSON response from server as dictionary
        """
        request = {
            "action": "chat_message",
            "data": {"node": chat_id, "last_message": -1, "content": text}
        }

        objects = [
            {
                "type": "chat_node",
                "id": chat_id,
                "tag": "00000000",
                "data": {"node": chat_id, "last_message": -1, "content": ""}
            }
        ]

        response = await self._send_request(
            method="POST",
            url="/runner/",
            data={
                "objects": json.dumps(objects),
                "request": json.dumps(request),
                "csrf_token": csrf_token
            }
        )

        data = await response.json()
        return data

