from typing import TYPE_CHECKING

from funpay.html import ReviewsHtmlParser
from .base_service import BaseService

if TYPE_CHECKING:
    from funpay.models import Review


class ReviewsService(BaseService):
    """Service for retrieving and managing user reviews on FunPay.

    Provides methods to fetch and parse review data from user profiles.
    Handles all review-related operations including retrieval and parsing.

    Args:
        requester (Requester): Authenticated HTTP requester instance
        account (Account): User account containing ID and auth data

    Attributes:
        requester (Requester): HTTP client for making requests
        account (Account): Authenticated user account info
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

        users_html = await self.requester.load_users_page(self.account.id)
        return ReviewsHtmlParser(users_html).parse()
