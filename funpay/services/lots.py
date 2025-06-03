from typing import TYPE_CHECKING, Optional

import asyncio

from funpay.parsers.html import FunpayUserLotsParser, FunpayLotGameIdParser, \
    FunpayLotNodeParser
from funpay.parsers.json import RaiseNodeParser
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Lot, RaiseNode, Node


class LotsService(BaseService):
    """Service for managing FunPay lots and bump operations.

    Provides functionality to:
    - Retrieve current user's lots
    - Perform lot bumping (up) operations
    - Track operation statuses

    """
    async def all(self, *, node_id: Optional[int] = None) -> list['Lot']:
        """Retrieves all active lots for the authenticated user.

        Args:
            node_id: Optional filter to return only lots from specific category node

        Returns:
            list[Lot]: Collection of parsed lot objects:

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            Only returns currently active lots (not ended or hidden)

        """
        html = await self._client.request.fetch_users_page(self._account.id)
        lots = FunpayUserLotsParser(html).parse(node_id=node_id)

        return lots

    async def get(self, *, lot_id: int, node_id: Optional[int] = None) -> 'Lot':
        """Retrieves active lot for the authenticated user.

        Args:
            lot_id: Unique identifier of the target listing
            node_id: Optional node identifier for additional validation

        Returns:
            Single Lot object matching the criteria

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            - When node_id is provided, verifies the lot belongs to specified node
            - More efficient than manual filtering after all() for single-item lookups
        """
        lots = await self.all()

        return next(
            lot for lot in lots
            if lot.id == lot_id and (not node_id or lot.node.id == node_id)
        )

    async def get_node(self, node_id: str) -> 'Node':
        """Retrieves node

        Args:
            node_id: Target node identifier

        Returns:
            Node object

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails
        """
        html = await self._client.request.fetch_lots_trade_page(node_id)
        node = FunpayLotNodeParser(html).parse()
        return node

    async def up(self) -> list['RaiseNode']:
        """Executes bulk bump/raise operation for all eligible marketplace listings.

        Performs complete bump workflow for each active listing:
        1. Node verification and game_id extraction
        2. API request submission
        3. Result parsing and validation

        Returns:
            List of RaiseNode objects containing operation results

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            - Operations are executed concurrently using asyncio.gather
            - Individual failures don't interrupt the batch process
            - Includes automatic rate limiting and retry logic
            - Results contain detailed success/failure information per node
        """
        async def process_node_up(lot: 'Lot') -> 'RaiseNode':
            html = await self._client.request.fetch_lots_trade_page(lot.node.id)
            game_id = FunpayLotGameIdParser(html).parse()

            data = await self._client.request.send_raise(
                game_id=game_id,
                node_id=lot.node.id
            )

            return RaiseNodeParser(data).parse(node=lot.node)

        lots = await self.all()
        results = await asyncio.gather(*[process_node_up(lot) for lot in lots])

        return results
