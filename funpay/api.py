from typing import Optional, TYPE_CHECKING

from funpay.http import AioHttpClient, BaseClient
from funpay.services import LotsService, ReviewsService
from funpay.parsers.html import AccountParserData

if TYPE_CHECKING:
    from funpay.types import Account


class FunpayAPI:
    """Main services for interacting with FunPay API.

    Provides a comprehensive interface for FunPay operations including:
    - Account management
    - Lot operations
    - Review handling
    - Lot up functionality

    Args:
        golden_key (str): Account authentication key (golden_key from cookies)
        client (Optional[BaseClient]): Custom HTTP services instance. If None,
            a default Requester will be initialized.

    Attributes:
        golden_key (str): Stored authentication key
        _client (BaseClient): HTTP services for making requests
        _account (Optional[Account]): Cached account data

    Note:
        The class implements lazy initialization - account data is only loaded
        after calling login() method.
    """

    def __init__(self, golden_key: str, *, client: Optional['BaseClient'] = None):
        self.golden_key = golden_key

        self._client = client if client else AioHttpClient(golden_key)
        self._account = None

    async def __aenter__(self) -> 'FunpayAPI':
        return await self.login()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.session.close()

    @property
    def account(self) -> 'Account':
        return self._account

    @property
    def lots(self) -> 'LotsService':
        return LotsService(self._account, self._client)

    @property
    def reviews(self) -> 'ReviewsService':
        return ReviewsService(self._account, self._client)

    async def login(self) -> 'FunpayAPI':
        """Authenticates the user and initializes account data.

        Performs the following operations:
        1. Makes an authenticated request to the main page
        2. Parses the HTML response to extract account details
        3. Initializes the Account object

        Returns:
            FunpayAPI: Returns self for method chaining
        """

        self._account = await self._client.request(parser=AccountParserData).auth()
        return self

    async def message_listener(self):
        pass

    async def order_listener(self):
        pass
