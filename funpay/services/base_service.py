from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from funpay.models import Account
    from funpay.requester import Requester


class BaseService:
    def __init__(self, account: 'Account', requester: 'Requester'):
        self._account = account
        self._requester = requester

    @property
    def account(self) -> 'Account':
        return self._account

