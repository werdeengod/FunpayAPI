from typing import TypeVar, Generic, Literal, Any
from abc import ABC, abstractmethod


from fake_useragent import FakeUserAgent
from aiocache import cached


T = TypeVar('T')


class BaseClient(ABC, Generic[T]):
    """Abstract Base Class defining the interface for http management.

    Provides the contract for implementing different http handlers
    with consistent behavior across implementations.

    Type Parameters:
        T: The type of http object to be managed (e.g., aiohttp.ClientSession)

    Class Attributes:
        BASE_URL (str): Base API endpoint URL (default: FunPay's production)

    Methods:
        get(): Retrieves the active http instance
        close(): Cleanly terminates the http

    Note:
        This is an abstract class that must be subclassed to create
        concrete http implementations.
    """

    BASE_URL: str = 'https://funpay.com'

    def __init__(self, golden_key: str):
        self.golden_key = golden_key
        self.session = None

    @abstractmethod
    def get_session(self) -> T:
        """Retrieve the active http instance.

        Returns:
            T: The managed http object of specified type
        """
        pass

    @abstractmethod
    async def close(self):
        """Cleanly shutdown the http."""
        pass

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
                "Origin": self.BASE_URL,
                "Referer": f"{self.BASE_URL}/"
            })

        return base_headers

    @abstractmethod
    async def request(self, method: Literal['GET', 'POST'], url: str, **kwargs) -> Any:
        """Execute authenticated HTTP request (main interface).

        Args:
            method: HTTP method ("GET" or "POST")
            url: Endpoint URL (relative to core)
            **kwargs: Additional arguments for aiohttp request

        Returns:
            aiohttp.ClientResponse: Response object

        Raises:
            APIError: For status codes >= 400 (via APIErrorFactory)

        Note:
            Responses are cached for 10 seconds (TTL) to prevent
            duplicate requests to the same endpoint.
        """
        pass
