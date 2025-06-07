from typing import TYPE_CHECKING, Optional, Literal

from funpay.parsers.html import FunpayUserReviewsHtmlParser, ReviewHtmlParser
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
    async def all(self, *, only_user_id: Optional[int] = None) -> list['Review']:
        """Retrieves reviews with optional username filtering.

        Args:
            only_user_id: Optional filter to return only reviews from specific user
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
        """

        html = await self.client.request.fetch_users_page(self._account.id)
        reviews = FunpayUserReviewsHtmlParser(html).parse(only_user_id=only_user_id)

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
        """
        reviews = await self.all()

        review = next(
            (review for review in reviews
             if order_code == review.order_code),
            None
        )

        return review

    async def send(self, text: str, *, order_code: str, rating: Literal[1, 2, 3, 4, 5] = 5) -> 'Review':
        """Submits a new / edit review for a completed order.

        This method handles the complete review submission process including:
        - Validation of review content
        - Rating assignment
        - Authentication via CSRF token
        - API request execution

        Args:
            text: Review content text
            order_code: Unique identifier of the order being reviewed
            rating: Star rating (1-5), defaults to 5 (highest)
                - 1: Very dissatisfied
                - 2: Dissatisfied
                - 3: Neutral
                - 4: Satisfied
                - 5: Very satisfied

        Returns:
            Review: content review
        Raises:
            HttpRequestError: For API failures (status >= 400)
        """
        html = await self.client.request.send_review(
            author_id=self._account.id,
            text=text,
            order_code=order_code,
            rating=rating,
            csrf_token=self._account.csrf_token
        )

        review = ReviewHtmlParser(html).parse()
        return review

    async def delete(self, *, order_code: str) -> bool:
        """Permanently removes a submitted review.

        Handles review deletion workflow including:
        - Ownership verification (author_id match)
        - CSRF-protected deletion request
        - System confirmation

        Args:
            order_code: The order code associated with review to delete

        Returns:
            bool: success operation

        Raises:
            HttpRequestError: For API communication failures
        """
        await self.client.request.delete_review(
            author_id=self._account.id,
            order_code=order_code,
            csrf_token=self._account.csrf_token
        )

        return True
