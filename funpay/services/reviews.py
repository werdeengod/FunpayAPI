from typing import TYPE_CHECKING

from funpay.parsers.html import AccountParserReviews
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Review


class ReviewsService(BaseService):
    """Service for retrieving and managing user reviews on FunPay.

    Provides methods to fetch and parse review data from user profiles.
    Handles all review-related operations including retrieval and parsing.

    """

    async def get(self) -> list['Review']:
        """Retrieves all reviews for the authenticated user.

        Workflow:
        1. Fetches user profile page HTML
        2. Parses review data using ReviewsHtmlParser
        3. Returns structured review objects

        Returns:
            list[Review]: Collection of parsed review objects
            with all available review data

        """

        reviews = await self.client.request(parser=AccountParserReviews).fetch_user_data(self.account.id)
        return reviews
