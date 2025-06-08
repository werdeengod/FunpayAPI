from typing import TYPE_CHECKING, Callable, Awaitable
from functools import wraps
import logging
import asyncio

from funpay.utils import random_tag
from funpay.enums import EventType
from .exceptions import ListenerError

if TYPE_CHECKING:
    from funpay import FunpayAPI


class _SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


class Runner(metaclass=_SingletonMeta):
    def __init__(self, api: 'FunpayAPI'):
        self.api = api
        self.logging = logging.getLogger('funpay.Runner')

        self._listeners = {}
        self._tasks = set[asyncio.Task]()
        self._is_running = False
        self._stop_event = asyncio.Event()

        self._first_request = True
        self._last_message_event_tag = random_tag()
        self._last_order_event_tag = random_tag()

        self._saved_orders = []
        self._last_messages = {}

    async def _get_updates(self) -> dict:
        updates = await self.api.client.request.fetch_updates(
            account_id=self.api.account.id,
            last_order_event_tag=self._last_order_event_tag,
            last_message_event_tag=self._last_message_event_tag,
            csrf_token=self.api.account.csrf_token
        )

        events = []
        for obj in updates['objects']:
            if obj.get("type") == "chat_bookmarks":
                self._last_message_event_tag = obj.get('tag', random_tag())
            elif obj.get("type") == "orders_counters":
                self._last_order_event_tag = obj.get('tag', random_tag())

        return updates

    def listener(self, event_name: EventType | str, *, interval: int = 6):
        if isinstance(event_name, str):
            event_name = EventType(event_name)

        if interval < 6:
            raise ListenerError("The interval is too small. Must be >=6")

        def decorator(func: Callable[..., Awaitable]):
            @wraps(func)
            async def wrapper():
                self.logging.info(
                    f"SET Listener={func.__name__}() "
                    f"Event={event_name} "
                    f"Interval={interval}"
                )

                while True:
                    if not self.api.account:
                        await self.api.login()

                    get_updates = await self._get_updates()

                    if get_updates.get('objects'):
                        if event_name == EventType.ORDER:
                            pass

                        await func(update=get_updates)

                    await asyncio.sleep(interval)

            self._listeners[event_name] = wrapper
            return wrapper

        return decorator

    @staticmethod
    async def _run_listener(listener: Callable[..., Awaitable]) -> None:
        try:
            await listener()
        except asyncio.CancelledError:
            return
        except Exception as e:
            raise e

    async def start(self) -> None:
        if self._is_running:
            return

        self._is_running = True

        for listener in self._listeners.values():
            loop = asyncio.get_event_loop()
            task = loop.create_task(self._run_listener(listener))
            self._tasks.add(task)

    async def stop(self) -> None:
        if not self._is_running:
            return

        self._is_running = False
        self._stop_event.set()

        for task in self._tasks:
            task.cancel()

        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def run_forever(self) -> None:
        if self._is_running:
            return

        try:
            await self.start()
            await self._stop_event.wait()
        except KeyboardInterrupt:
            await self.stop()
