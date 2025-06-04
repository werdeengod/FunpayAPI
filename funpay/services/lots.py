from typing import TYPE_CHECKING, Optional

import asyncio

from funpay.parsers.html import FunpayUserLotsHtmlParser, FunpayGamesHtmlParser
from funpay.parsers.json import RaiseNodeJsonParser
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Lot, RaiseNode, Game


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
            node_id: Optional filter to return only lots from specific node

        Returns:
            list[Lot]: Collection of parsed lot objects:

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            Only returns currently active lots (not ended or hidden)

        """
        html = await self._client.request.fetch_users_page(self._account.id)
        lots = FunpayUserLotsHtmlParser(html).parse(node_id=node_id)

        return lots

    async def get(self, *, lot_id: int) -> 'Lot':
        """Retrieves active lot for the authenticated user.

        Args:
            lot_id: Unique identifier of the target listing

        Returns:
            Single Lot object matching the criteria

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            - More efficient than manual filtering after all() for single-item lookups
        """
        lots = await self.all()

        return next(
            (lot for lot in lots
             if lot.id == lot_id),
            None
        )

    async def _get_game_from_node_id(self, node_id: int) -> 'Game':
        """Returns the Game containing the specified node_id with O(n) complexity."""

        html = await self._client.request.fetch_main_page()
        games = FunpayGamesHtmlParser(html).parse()

        return next(
            (game for game in games
             if any(node.id == node_id for node in game.nodes)),
            None
        )

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
        """

        async def process_node_up(lot: 'Lot') -> 'RaiseNode':
            game = await self._get_game_from_node_id(lot.node.id)
            data = await self._client.request.send_raise(
                game_id=game.id,
                node_id=lot.node.id
            )

            return RaiseNodeJsonParser(data).parse(node=lot.node)

        results = await asyncio.gather(*[
            process_node_up(lot)
            for lot in await self.all()
        ])

        return results
