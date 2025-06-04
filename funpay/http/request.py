from typing import TYPE_CHECKING, Literal, TypeVar, Generic
import json

from fake_useragent import FakeUserAgent
from aiocache import cached

from funpay.http.exceptions import HttpRequestError
from funpay.enums import ResponseType

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

    def _get_headers(self, response_type: 'ResponseType') -> dict:
        """Generate appropriate HTTP headers for the request method."""

        base_headers = {
            "User-Agent": FakeUserAgent().random,
            "Cookie": f"golden_key={self.client.golden_key}",
            "Accept": "application/json, text/html",
            "Connection": "keep-alive"
        }

        if response_type == ResponseType.JSON:
            base_headers.update({
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": self.client.BASE_URL,
                "Referer": f"{self.client.BASE_URL}/"
            })

        return base_headers

    async def _send_request(
        self,
        *,
        method: Literal["POST", "GET"],
        url: str,
        response_type: 'ResponseType',
        **kwargs: dict
    ) -> T:
        """Core method for sending HTTP requests with built-in error handling.

        Handles:
        - Session management
        - Header injection
        - Error response detection
        - Request execution

        Args:
            method: HTTP verb ("POST" or "GET")
            url: Endpoint path (relative to base URL)
            **kwargs: Additional arguments for aiohttp request

        Returns:
            The response object (type depends on caller's processing)

        Raises:
            HttpRequestError: For any 4xx/5xx status code responses
        """
        session = self.client.get_session()

        response = await session.request(
            method=method,
            url=url,
            headers=self._get_headers(response_type),
            **kwargs
        )

        if response.status >= 400:
            raise HttpRequestError(
                status=response.status,
                url=url,
                text=await response.text()
            )

        return response

    @cached(ttl=3600)
    async def fetch_main_page(self) -> str:
        """Retrieves the platform's main page HTML content.

        Note:
            - Heavily cached (1 hour TTL) as this data rarely changes
            - Contains essential site structure and metadata

        Returns:
            Raw HTML string of the main landing page
        """
        response = await self._send_request(
            method='GET',
            url='/',
            response_type=ResponseType.TEXT
        )

        return await response.text()

    @cached(ttl=30)
    async def fetch_users_page(self, account_id: int) -> str:
        """Fetches user profile page HTML by account ID.

        Args:
            account_id: Unique platform identifier for target user

        Returns:
            HTML content string containing:
            - User profile information
            - Review data
            - Listing information
        """
        response = await self._send_request(
            method="GET",
            url=f'/users/{account_id}/',
            response_type=ResponseType.TEXT
        )

        return await response.text()

    @cached(ttl=30)
    async def fetch_lots_page(self, game_id: int) -> str:
        """Retrieves lots page HTML for specific marketplace node.

        Args:
            game_id: Unique category/node identifier

        Returns:
            HTML string with:
            - Lot listings
            - Trading rules
            - Node-specific metadata
        """
        response = await self._send_request(
            method="GET",
            url=f'/lots/{game_id}/',
            response_type=ResponseType.TEXT
        )

        return await response.text()

    async def send_raise(self, game_id: str, node_id: str) -> dict:
        """Submits a bump/raise request for marketplace listings.

        Args:
            game_id: Game session identifier
            node_id: Target marketplace node ID

        Returns:
            API response containing:
            - Operation status
            - Updated listing data
            - Cooldown information
        """
        response = await self._send_request(
            method='POST',
            url='/lots/raise',
            response_type=ResponseType.JSON,
            data={
                "game_id": game_id,
                "node_id": node_id
            }
        )

        data = await response.json()
        return data

    async def send_message(self, chat_id: str | int, text: str, csrf_token: str) -> dict:
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
            response_type=ResponseType.JSON,
            data={
                "objects": json.dumps(objects),
                "request": json.dumps(request),
                "csrf_token": csrf_token
            },
        )

        data = await response.json()
        return data

    async def fetch_order_update(self, account_id, last_order_event_tag: str, csrf_token: str) -> dict:
        """Checks for order status updates.

        Args:
            account_id: Authenticated user's ID
            last_order_event_tag: Previous update marker
            csrf_token: Current CSRF token

        Returns:
            Order update payload containing:
            - New events
            - Status changes
            - Counter updates
        """
        orders = {
            "type": "orders_counters",
            "id": account_id,
            "tag": last_order_event_tag,
            "data": False
        }

        response = await self._send_request(
            method="POST",
            url='/runner/',
            response_type=ResponseType.JSON,
            data={
                "objects": json.dumps(orders),
                "request": False,
                "csrf_token": csrf_token
            },
        )

        return await response.json()

    async def send_review(self, author_id: int, text: str, rating: int, csrf_token: str, order_code: str) -> str:
        """Submits review for completed order.

        Args:
            author_id: Reviewer's account ID
            text: Review content
            rating: Numeric rating (typically 1-5)
            csrf_token: Current CSRF token
            order_code: Associated order ID

        Returns:

        """
        response = await self._send_request(
            method="POST",
            url='/orders/review',
            response_type=ResponseType.JSON,
            data={
                "authorId": author_id,
                "text": text,
                "rating": rating,
                "csrf_token": csrf_token,
                "orderId": order_code
            }
        )

        data = await response.json()
        return data.get("content")

    async def delete_review(self, author_id: int, order_code: str, csrf_token: str) -> str:
        """Removes previously submitted review.

        Args:
            author_id: Reviewer's account ID
            order_code: Original order ID
            csrf_token: Current CSRF token

        Returns:

        """
        response = await self._send_request(
            method="POST",
            url="/orders/reviewDelete",
            response_type=ResponseType.JSON,
            data={
                "authorId": author_id,
                "csrf_token": csrf_token,
                "orderId": order_code
            }
        )

        data = await response.json()
        return data.get("content")

    async def fetch_chat_history(self, chat_id: int, last_message: int) -> dict | None:
        response = await self._send_request(
            method="GET",
            url=f"/chat/history",
            response_type=ResponseType.JSON,
            params={
                "node": chat_id,
                "last_message": last_message
            }
        )

        data = await response.json()
        chat = data.get("chat")

        if isinstance(chat, dict):
            return chat
