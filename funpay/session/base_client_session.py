import aiohttp
from .session_abc import SessionABC


class BaseClientSession(SessionABC[aiohttp.ClientSession]):
    def get(self) -> 'aiohttp.ClientSession':
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                base_url=self.BASE_URL
            )

        return self.session

    async def close(self) -> None:
        if self.session:
            await self.session.close()

