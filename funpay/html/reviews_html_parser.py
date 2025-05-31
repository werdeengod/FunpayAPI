from typing import TYPE_CHECKING

from funpay.models import Review
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class ReviewsHtmlParser(BaseHtmlParser):
    def _extract_reviews_container(self) -> list['Tag']:
        return self.soup.find_all("div", {"class": "review-container"})

    def parse(self) -> list['Review']:
        review_containers = self._extract_reviews_container()
        reviews = []

        for review in review_containers:
            username = review.find("div", {"class": "media-user-name"}).text
            order_code = review.find("div", {"class": "review-item-order"}).text
            date = review.find("div", {"class": "review-item-date"}).text
            text = review.find("div", {"class": "review-item-text"}).text.strip()

            reviews.append(Review(
                username=username,
                order_code=order_code,
                date=date,
                text=text
            ))

        return reviews