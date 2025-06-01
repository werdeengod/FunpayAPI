from typing import TYPE_CHECKING

import asyncio

from funpay.parsers.html import AccountParserNodes, AccountParserLots, LotsTradeParserGameData
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Lot


class LotsService(BaseService):
    """Service for managing FunPay lots and bump operations.

    Provides functionality to:
    - Retrieve current user's lots
    - Perform lot bumping (up) operations
    - Track operation statuses

    """

    async def get(self) -> list['Lot']:
        """Retrieves all active lots for the authenticated user.

        Returns:
            list[Lot]: Collection of parsed lot objects:

        Note:
            Only returns currently active lots (not ended or hidden)

        """

        lots = await self.client.request(parser=AccountParserLots).fetch_user_data(self.account.id)
        return lots

    async def up(self) -> dict:
        """Performs bump (up) operation for all available lots.

        Workflow:
        1. Fetches user's lots page
        2. Extracts all lot node IDs
        3. Sends bump request for each lot category
        4. Returns operation statuses

        Returns:
            dict[str, str]: Mapping of node IDs to operation results
            Example: {'123': '1', '456': '0'}
        """

        async def process_node(node_id: str) -> None:
            game_id = await self.client.request(parser=LotsTradeParserGameData).fetch_lots_trade_data(node_id)
            data = await self.client.request().send_raise_request(game_id, node_id)

            return data

        nodes = await self.client.request(parser=AccountParserNodes).fetch_user_data(self.account.id)
        results = await asyncio.gather(*[process_node(node) for node in nodes])

        return results
