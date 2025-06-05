from typing import TYPE_CHECKING, Callable, Awaitable
import asyncio

from funpay.utils import random_tag

if TYPE_CHECKING:
    from funpay import FunpayAPI


class Runner:
    def __init__(self, api: 'FunpayAPI'):
        self.api = api

        self._last_message_event_tag = random_tag()
        self._last_order_event_tag = random_tag()

    async def get_updates(self) -> dict:
        return await self.api.client.request.fetch_updates(
            account_id=self.api.account.id,
            last_order_event_tag=self._last_order_event_tag,
            csrf_token=self.api.account.csrf_token
        )

    def listener(self, func: Callable[..., Awaitable]):
        async def wrapper(*args, **kwargs):
            while True:
                if not self.api.account:
                    await self.api.login()

                get_updates = await self.get_updates()

                if get_updates.get('objects'):
                    await func(*args, *kwargs, update=get_updates)

                await asyncio.sleep(6)

        return wrapper
