from typing import TYPE_CHECKING

from funpay.parsers.html import AccountParserLots, LotsTradeParserGameData
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Lot


class LotsService(BaseService):
    """Manager for managing FunPay lots and bump operations.

    Provides functionality to:
    - Retrieve current user's lots
    - Perform lot bumping (up) operations
    - Track operation statuses

    Args:
        client (BaseClient): Authenticated HTTP requester instance
        account (Account): User account containing ID and auth data

    Attributes:
        client (BaseClient): HTTP services for making requests
        account (Account): Authenticated user account info
    """

    async def get(self) -> list['Lot']:
        """Retrieves all active lots for the authenticated user.

        Returns:
            list[Lot]: Collection of parsed lot objects:

        Note:
            Only returns currently active lots (not ended or hidden)

        """

        html = await self.client.load_users_page_html(self.account.id)
        return AccountParserLots(html).parse()

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

        users_html = await self.client.load_users_page_html(self.account.id)
        nodes = AccountParserLots(users_html).extract_nodes_id()
        state = {}

        for node_id in nodes:
            lots_html = await self.client.load_lots_trade_page_html(node_id)
            game_id = LotsTradeParserGameData(lots_html).parse()

            response = await self.client.request(
                method='POST',
                url='/lots/raise',
                data={
                    "game_id": game_id,
                    "node_id": node_id
                }
            )

            data = await response.json()
            state[node_id] = data['error']

        return state
