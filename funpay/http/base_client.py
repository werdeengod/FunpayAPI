from typing import TypeVar, Generic, Type, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from funpay.parsers import ABCParser
    from .request import Request


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

    @abstractmethod
    def request(self, *, parser: Optional[Type['ABCParser']] = None) -> 'Request':
        """Factory method for creating Request instances.

        Implementations should return a properly configured Request handler
        with the specified parser.

        Args:
            parser: Optional parser class for automatic response processing

        Returns:
            Request: Configured request handler instance

        Note:
            This is the primary entry point for all API requests.
            Concrete clients must implement this method.
        """
        pass
