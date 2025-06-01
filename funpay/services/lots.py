from typing import TYPE_CHECKING

import asyncio

from funpay.parsers.html import FunpayUserNodeIdsParser, FunpayUserLotsParser, FunpayLotGameIdParser
from funpay.parsers.json import RaiseNodeParser
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Lot, RaiseNode


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

        html = await self.client.request.fetch_users_page(self.account.id)
        lots = FunpayUserLotsParser(html).parse()
        return lots

    async def up(self) -> list['RaiseNode']:
        """Performs a batch 'raise' (bump) operation for all available user lots/nodes.

        This method automates the process of bumping multiple listings on FunPay by:
        1. Fetching all user's node IDs from their profile
        2. Processing each node individually to:
           - Extract required game_id from the trade page
           - Send raise request to the API
        3. Returning structured results for each operation

        Workflow:
            1. Fetch user's profile page HTML
            2. Parse all node IDs where lots can be raised
            3. For each node:
                a. Load its trade page HTML
                b. Extract game_id from the page
                c. Submit raise request via API
                d. Parse and store the result
            4. Return aggregated results

        Returns:
            list[RaiseNode]

        Raises:
            HttpRequestError: If any API request fails (status >= 400)
            ParserError: If HTML parsing fails for game_id extraction

        Note:
            - Uses asyncio.gather for concurrent processing
            - Each node is processed independently
            - Failed operations don't stop the batch (exceptions are caught)
        """
        async def process_node_up(node_id: str) -> 'RaiseNode':
            html = await self.client.request.fetch_lots_trade_page(node_id)
            game_id = FunpayLotGameIdParser(html).parse()

            data = await self.client.request.send_raise(
                game_id=game_id,
                node_id=node_id
            )
            data['node_id'] = node_id

            return RaiseNodeParser(data).parse()

        users_html = await self.client.request.fetch_users_page(self.account.id)
        nodes = FunpayUserNodeIdsParser(users_html).parse()

        results = await asyncio.gather(*[process_node_up(node) for node in nodes])
        return results
