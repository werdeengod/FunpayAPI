from typing import TYPE_CHECKING, Type, Literal, TypeVar, Generic, Any, Optional

from fake_useragent import FakeUserAgent
from aiocache import cached

from funpay.http.exceptions import HttpRequestError

if TYPE_CHECKING:
    from funpay.types import Account
    from funpay.parsers import ABCParser
    from funpay.http import BaseClient

T = TypeVar('T')


class Request(Generic[T]):
    """Handles HTTP requests and response processing for the API client.

    This class serves as the core transport mechanism, providing:
    - Pre-configured headers with authentication
    - Request/response lifecycle management
    - Automatic parsing of responses
    - Caching for frequent requests

    Type Variables:
        T: The type of raw response object (aiohttp.ClientResponse, requests.Response, etc.)

    Args:
        client: Reference to the parent BaseClient instance
        parser: Optional parser class for automatic response processing

    Attributes:
        client (BaseClient): The parent client instance
        _parser (Optional[Type[BaseParser]]): Response parser class if provided
    """

    def __init__(self, client: 'BaseClient', parser: Optional[Type['ABCParser']] = None):
        self.client = client
        self._parser = parser

    def _get_headers(self, method: Literal["POST", "GET"]) -> dict:
        """Generates headers for HTTP requests with authentication.

        Args:
            method: The HTTP method to generate headers for

        Returns:
            dict: Complete headers dictionary including:
                - Base headers (UA, cookies)
                - POST-specific headers when applicable
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
        """Executes the HTTP request with caching.

        Args:
            method: HTTP method (GET/POST)
            url: Endpoint URL (relative to BASE_URL)
            **kwargs: Additional arguments for the request

        Returns:
            T: Raw response object from the HTTP library

        Raises:
            HttpRequestError: For 4xx/5xx status codes
        """
        session = self.client.get_session()

        response = await session.request(
            method=method,
            url=url,
            headers=self._get_headers(method),
            **kwargs
        )

        if response.status >= 400:
            raise HttpRequestError

        return response

    async def _get_parse_data(self, response: T, *, parse_type: Literal["html", "json"]) -> Any:
        """Processes raw response through configured parser.

        Args:
            response: Raw HTTP response
            parse_type: Expected response format ('html' or 'json')

        Returns:
            Any: Parsed data if parser exists, raw response otherwise
        """

        if not self._parser:
            return response

        if parse_type == "html":
            parse = self._parser(await response.text()).parse()
        else:
            parse = self._parser(await response.json()).parse()

        return parse

    async def fetch_account(self) -> 'Account':
        """Authenticates and fetches current user account data.

        Returns:
            Account: Authenticated user account details
        """
        response = await self._send_request(
            method='GET',
            url='/'
        )

        return await self._get_parse_data(
            response,
            parse_type="html"
        )

    async def fetch_user_data(self, account_id: int) -> Any:
        """Retrieves public profile data for a user.

        Args:
            account_id: Target user ID

        Returns:
            Any: Parsed profile data if parser exists, raw HTML otherwise
        """
        response = await self._send_request(
            method="GET",
            url=f'/users/{account_id}/'
        )

        return await self._get_parse_data(
            response,
            parse_type="html"
        )

    async def fetch_lots_trade_data(self, node_id: int) -> Any:
        """Fetches trading data for specific lot category.

        Args:
            node_id: Category/node identifier

        Returns:
            Any: Parsed trading data if parser exists, raw HTML otherwise
        """
        response = await self._send_request(
            method="GET",
            url=f'/lots/{node_id}/trade'
        )

        return await self._get_parse_data(
            response,
            parse_type="html"
        )

    async def send_raise_request(self, game_id: str, node_id: str) -> dict:
        """Submits a 'bump' request for a lot.

        Args:
            game_id: Game identifier
            node_id: Category/node identifier

        Returns:
            dict: Raw JSON response from server
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
