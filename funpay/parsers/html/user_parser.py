from typing import TYPE_CHECKING, Optional
import json

from funpay.enums import Locale
from funpay.types import Account, Lot, Review, Node
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class FunpayUserProfileParser(BaseHtmlParser):
    def _extract_account_data(self) -> dict:
        return json.loads(self.soup.find("body")["data-app-data"])

    def _extract_account_username(self) -> str:
        return self.get_text(self.soup, "div.user-link-name")

    def _extract_balance(self) -> int | None:
        balance = self.get_text(self.soup, "span.badge.badge-balance", to_type=int)
        return balance

    def _parse_implementation(self) -> 'Account':
        data = self._extract_account_data()

        return Account(
            id=int(data['userId']),
            csrf_token=data['csrf-token'],
            username=self._extract_account_username(),
            balance=self._extract_balance(),
            locale=Locale(data['locale'])
        )


class FunpayUserLotsParser(BaseHtmlParser):
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


class FunpayUserReviewsParser(BaseHtmlParser):
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

