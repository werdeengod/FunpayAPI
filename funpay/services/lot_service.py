from funpay.parser import LotParser
from .base_service import BaseService


class LotService(BaseService):
    async def _get_nodes_id(self) -> list[str]:
        response = await self._requester(
            method='get',
            url=f'/users/{self.account.id}/'
        )

        html = await response.text()
        return LotParser(html).get_nodes_id()

    async def up(self) -> dict:
        nodes = await self._get_nodes_id()
        state = {}

        for node_id in nodes:
            response = await self._requester(
                method='get',
                url=f'/lots/{node_id}/trade'
            )

            html = await response.text()
            game_id = LotParser(html).get_game_id()

            response = await self._requester(
                method='post',
                url='/lots/raise',
                data={
                    "game_id": game_id,
                    "node_id": node_id
                }
            )

            data = await response.json()
            state[node_id] = data['error']

        return state
