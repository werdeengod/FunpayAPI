from typing import TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar('T')


class SessionABC(ABC, Generic[T]):
    """Abstract Base Class defining the interface for session management.

    Provides the contract for implementing different session handlers
    with consistent behavior across implementations.

    Type Parameters:
        T: The type of session object to be managed (e.g., aiohttp.ClientSession)

    Class Attributes:
        BASE_URL (str): Base API endpoint URL (default: FunPay's production)

    Methods:
        get(): Retrieves the active session instance
        close(): Cleanly terminates the session

    Note:
        This is an abstract class that must be subclassed to create
        concrete session implementations.
    """

    BASE_URL: str = 'https://funpay.com'

    def __init__(self):
        self.session = None

    @abstractmethod
    def get(self) -> T:
        """Retrieve the active session instance.

        Returns:
            T: The managed session object of specified type
        """
        pass

    @abstractmethod
    async def close(self):
        """Cleanly shutdown the session."""
        pass
