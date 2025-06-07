from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from funpay.types import Account
    from funpay.http import AioHttpClient


class BaseService:
    """Base class for API service implementations.

    Provides common functionality for services that require:
    - Authenticated HTTP client access
    - Account-specific operations

    Args:
        account (Account): The authenticated user account.
        client (AioHttpClient): An async HTTP client for API requests.
    """

    def __init__(self, account: 'Account', client: 'AioHttpClient'):
        self._account = account
        self.client = client
