from typing import TYPE_CHECKING, Optional

from funpay.parsers.html import FunpayUserReviewsParser
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Review


class ReviewsService(BaseService):
    """Service for comprehensive review management on FunPay.

    Handles the complete review lifecycle including:
    - Retrieval and filtering of user reviews
    - Review submission (WIP)
    - Review deletion (WIP)
    - Review analysis and statistics
    """
    async def all(self, *, username: Optional[str] = None) -> list['Review']:
        """Retrieves reviews with optional username filtering.

        Args:
            username: Optional filter to return only reviews from specific user
                     Case-insensitive comparison

        Returns:
            List of Review objects containing:
            - Review content and rating
            - Associated order information
            - Author metadata
            - Timestamps

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Workflow:
            1. Fetches complete user profile HTML
            2. Extracts and parses review data
            3. Applies username filter if provided
            4. Returns structured review objects

        """

        html = await self._client.request.fetch_users_page(self._account.id)
        reviews = FunpayUserReviewsParser(html).parse(username=username)

        return reviews

    async def get(self, *, order_code: str) -> 'Review':
        """Retrieves a specific review by its associated order code.

        Args:
            order_code: Unique order identifier tied to the review

        Returns:
            Single Review object matching the order code

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Raises:
            StopIteration: When no matching review is found
        """
        reviews = await self.all()
        review = next((review for review in reviews if order_code == review.order_code))
        return review

    async def send_review(self):
        pass

    async def delete_review(self):
        pass
