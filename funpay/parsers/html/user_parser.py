from typing import TYPE_CHECKING, Optional

from funpay.types import Lot, Review, Node
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class FunpayUserProfileHtmlParser(BaseHtmlParser):
    """Parser for get profile from link https://funpay.com/users/{USER_ID}/"""
    pass


class FunpayUserLotsHtmlParser(BaseHtmlParser):
    """Parser for get lots from link https://funpay.com/users/{USER_ID}/"""

    def _extract_offer_container(self) -> list['Tag']:
        return self.soup.find_all("div", {"class": "offer"})

    def _parse_implementation(self, node_id: Optional[str] = None) -> list['Lot']:
        offers_soup = self._extract_offer_container()
        lots = []

        for offer in offers_soup:
            offer_header = offer.find("div", {"class": "offer-list-title-container"})
            offer_body = offer.find("a", {"class": "tc-item"})

            if not offer_header or not offer_body:
                continue

            node_link = offer_header.find("a")
            node = Node(
                id=int(node_link['href'].split('/')[-2]),
                name=node_link.text
            )

            if node_id and node_id != node.id:
                continue

            lot_id = int(offer_body['href'].split('=')[1])
            title = self.get_text(offer_body, "div.tc-desc-text")
            price = float(offer_body.find("div", {"class": "tc-price"})['data-s'])
            amount = self.get_text(offer_body, "div.tc-amount", int)

            lots.append(Lot(
                id=lot_id,
                node=node,
                title=title,
                price=price,
                amount=amount
            ))

        return lots


class FunpayUserReviewsHtmlParser(BaseHtmlParser):
    """Parser for get reviews from link https://funpay.com/users/{USER_ID}/"""

    def _extract_reviews_container(self) -> list['Tag']:
        return self.soup.find_all("div", {"class": "review-container"})

    def _parse_implementation(self, username: Optional[str] = None) -> list['Review']:
        review_containers = self._extract_reviews_container()
        reviews = []

        for review in review_containers:
            medial_username = self.get_text(review, "div.media-user-name")

            if username and username.lower() != medial_username:
                continue

            order_code = self.get_text(review, "div.review-item-order").split('#')[1]
            date = self.get_text(review, "div.review-item-date")
            text = self.get_text(review, "div.review-item-text")

            reviews.append(Review(
                username=medial_username,
                order_code=order_code,
                date=date,
                text=text
            ))

        return reviews

