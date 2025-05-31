from typing import Optional, TYPE_CHECKING

from funpay.requester import Requester
from funpay.services import LotsService, ReviewsService
from funpay.html import AccountHtmlParser

if TYPE_CHECKING:
    from funpay.models import Account


class FunpayAPI:
    """Main client for interacting with FunPay API.

    Provides a comprehensive interface for FunPay operations including:
    - Account management
    - Lot operations
    - Review handling
    - Lot up functionality

    Args:
        golden_key (str): Account authentication key (golden_key from cookies)
        requester (Optional[Requester]): Custom HTTP client instance. If None,
            a default Requester will be initialized.

    Attributes:
        golden_key (str): Stored authentication key
        _requester (Requester): HTTP client for making requests
        _account (Optional[Account]): Cached account data

    Note:
        The class implements lazy initialization - account data is only loaded
        after calling login() method.
    """

    def __init__(self, golden_key: str, *, requester: Optional[Requester] = None):
        self.golden_key = golden_key

        self._requester = requester if requester else Requester(golden_key)
        self._account = None

    async def __aenter__(self) -> 'FunpayAPI':
        return await self.login()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._requester.session.close()

    @property
    def account(self) -> 'Account':
        return self._account

    @property
    def lots(self) -> 'LotsService':
        return LotsService(self._account, self._requester)

    @property
    def reviews(self) -> 'ReviewsService':
        return ReviewsService(self._account, self._requester)

    async def login(self) -> 'FunpayAPI':
        """Authenticates the user and initializes account data.

        Performs the following operations:
        1. Makes an authenticated request to the main page
        2. Parses the HTML response to extract account details
        3. Initializes the Account object

        Returns:
            FunpayAPI: Returns self for method chaining
        """

        response = await self._requester(
            method='GET',
            url='/'
        )

        html = await response.text()
        self._account = AccountHtmlParser(html).parse()
        return self
