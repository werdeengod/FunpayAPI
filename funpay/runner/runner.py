from typing import TYPE_CHECKING

from funpay.utils import random_tag

if TYPE_CHECKING:
    from funpay.types import Account
    from funpay.http import AioHttpClient


class Runner:
    def __init__(self, account: 'Account', client: 'AioHttpClient'):
        self.account = account
        self.client = client

        self._last_message_event_tag = random_tag()
        self._last_order_event_tag = random_tag()

    async def get_order_update(self) -> dict:
        return await self.client.request.fetch_order_update(
            account_id=self.account.id,
            last_order_event_tag=self._last_order_event_tag,
            csrf_token=self.account.csrf_token
        )

    async def get_message_update(self) -> dict:
        pass
