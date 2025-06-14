from typing import Optional, TYPE_CHECKING, Union

from funpay.http import AioHttpClient, BaseClient
from funpay.services import LotsService, ReviewsService, ChatService, OrdersService
from funpay.runner import Runner
from funpay.parsers.html import FunpayAccountHtmlParser, FunpayUserProfileHtmlParser

if TYPE_CHECKING:
    from funpay.types import Account, User


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
        _golden_key (str): Stored authentication key
        client (BaseClient): HTTP services for making requests
        _account (Optional[Account]): Cached account data

    Note:
        The class implements lazy initialization - account data is only loaded
        after calling login() method.
    """

    def __init__(self, golden_key: Optional[str] = None, *, client: Optional['BaseClient'] = None):
        self._golden_key = golden_key
        self.client = client if client else AioHttpClient(golden_key)

        self._account = None

    async def __aenter__(self) -> 'FunpayAPI':
        return await self.login()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.session.close()

    @property
    def account(self) -> Union['Account', None]:
        """Provides access to the authenticated account.

        Returns:
            Account: The user account associated with this service.
        """
        return self._account

    @property
    def lots(self) -> 'LotsService':
        """Service for managing FunPay lots"""
        return LotsService(
            account=self.account,
            client=self.client
        )

    @property
    def reviews(self) -> 'ReviewsService':
        """Service for managing FunPay reviews"""
        return ReviewsService(
            account=self.account,
            client=self.client
        )

    @property
    def orders(self) -> 'OrdersService':
        """Service for managing FunPay orders"""
        return OrdersService(
            account=self.account,
            client=self.client
        )

    @property
    def chat(self) -> 'ChatService':
        """Service for managing chat operations and message handling"""
        return ChatService(
            account=self.account,
            client=self.client
        )

    def get_runner(self) -> 'Runner':
        return Runner(self)

    async def login(self) -> 'FunpayAPI':
        """Authenticates the user and initializes account data.

        Performs the following operations:
        1. Makes an authenticated request to the main page
        2. Parses the HTML response to extract account details
        3. Initializes the Account object

        Returns:
            FunpayAPI: Returns self for method chaining
        """

        html = await self.client.request.fetch_main_page()
        self._account = FunpayAccountHtmlParser(html).parse()
        return self

    async def get_user(self, user_id: int) -> 'User':
        html = await self.client.request.fetch_users_page(user_id)

        user = FunpayUserProfileHtmlParser(html).parse(
            locale=self.account.locale,
            user_id=user_id
        )

        return user
