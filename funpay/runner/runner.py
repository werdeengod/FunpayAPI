import json
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
        orders = {
            "type": "orders_counters",
            "id": self.account.id,
            "tag": self._last_order_event_tag,
            "data": False
        }

        response = await self.client.request(
            method="POST",
            url='/runner/',
            data={
                "objects": json.dumps(orders),
                "request": False,
                "csrf_token": self.account.csrf_token
            }
        )

        return await response.json()

    async def parse_order_update(self, update: dict):
        pass
