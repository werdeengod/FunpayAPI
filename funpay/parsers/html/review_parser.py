from typing import TYPE_CHECKING, Optional

from funpay.types import Review, UserCut
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class ReviewHtmlParser(BaseHtmlParser):
    def _extract_review_container(self) -> 'Tag':
        return self.soup.find("div", {"class": "review-container"})

    def _extract_media_user_name(self) -> 'Tag':
        return self.soup.find("div", {"class": "media-user-name"})

    def _parse_implementation(self) -> 'Review':
        review_container = self._extract_review_container()
        media_user_name = self._extract_media_user_name()

        if not media_user_name:
            user = UserCut(id=None, username=None)
        else:
            user_link = media_user_name.find("a")
            user = UserCut(
                id=int(user_link['href'].split('/')[-2]),
                username=user_link.text.strip()
            )

        order_code = review_container.get('data-order')
        if not order_code:
            order_code = self.get_text(review_container, "div.review-item-order").split('#')[1]

        date = self.get_text(review_container, "div.review-item-date")
        text = self.get_text(review_container, "div.review-item-text")

        return Review(
            user=user,
            order_code=order_code,
            date=date,
            text=text
        )


class FunpayUserReviewsHtmlParser(BaseHtmlParser):
    """Parser for get reviews from link:
       - https://funpay.com/users/{USER_ID}/
    """
    def _extract_reviews_container(self) -> list['Tag']:
        return self.soup.find_all("div", {"class": "review-container"})

    def _parse_implementation(self, only_user_id: Optional[int] = None) -> list['Review']:
        review_containers = self._extract_reviews_container()
        reviews = []

        for review_container in review_containers:
            review = ReviewHtmlParser(str(review_container)).parse()
            if not review or only_user_id and review.user_id != 0 and review.user_id != only_user_id:
                continue

            reviews.append(review)

        return reviews
