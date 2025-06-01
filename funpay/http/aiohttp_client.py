import aiohttp

from .base_client import BaseClient
from .request import Request


class AioHttpClient(BaseClient[aiohttp.ClientSession]):
    def get_session(self) -> 'aiohttp.ClientSession':
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                base_url=self.BASE_URL
            )

        return self.session

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    @property
    def request(self) -> 'Request':
        return Request[aiohttp.ClientResponse](self)
