from typing import TYPE_CHECKING
import json

from funpay.types import Account, Lot, Review
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class AccountParserData(BaseHtmlParser):
    def _extract_account_data(self) -> dict:
        return json.loads(self.soup.find("body")["data-app-data"])

    def _extract_account_username(self) -> str:
        return self.get_text(self.soup, "div.user-link-name")

    def _extract_balance(self) -> int | None:
        balance = self.get_text(self.soup, "span.badge.badge-balance", to_type=int)
        return balance

    def parse(self) -> 'Account':
        data = self._extract_account_data()

        return Account(
            id=int(data['userId']),
            csrf_token=data['csrf-token'],
            username=self._extract_account_username(),
            balance=self._extract_balance()
        )


class AccountParserLots(BaseHtmlParser):
    def _extract_offer_container(self, class_name: str) -> list['Tag']:
        return self.soup.find_all("div", {"class": class_name})

    def extract_nodes_id(self) -> list[str]:
        offers_soup = self._extract_offer_container("offer-list-title-container")
        nodes = []

        for offer in offers_soup:
            category_id = offer.find("a")['href'].split('/')[-2]
            nodes.append(category_id)

        return nodes

    def parse(self) -> list['Lot']:
        offers_soup = self._extract_offer_container("offer")
        lots = []

        for offer in offers_soup:
            offer_header = offer.find("div", {"class": "offer-list-title-container"})
            offer_body = offer.find("a", {"class": "tc-item"})

            if not offer_header or not offer_body:
                continue

            node_id = int(offer_header.find("a")['href'].split('/')[-2])
            title = self.get_text(offer_body, "div.tc-desc-text")
            price = float(offer_body.find("div", {"class": "tc-price"})['data-s'])
            amount = self.get_text(offer_body, "div.tc-amount", int)

            lots.append(Lot(
                node_id=node_id,
                title=title,
                price=price,
                amount=amount
            ))

        return lots


class AccountParserReviews(BaseHtmlParser):
    def _extract_reviews_container(self) -> list['Tag']:
        return self.soup.find_all("div", {"class": "review-container"})

    def parse(self) -> list['Review']:
        review_containers = self._extract_reviews_container()
        reviews = []

        for review in review_containers:
            username = self.get_text(review, "div.media-user-name")
            order_code = self.get_text(review, "div.review-item-order")
            date = self.get_text(review, "div.review-item-date")
            text = self.get_text(review, "div.review-item-text")

            reviews.append(Review(
                username=username,
                order_code=order_code,
                date=date,
                text=text
            ))

        return reviews

