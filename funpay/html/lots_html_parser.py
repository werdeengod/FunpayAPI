from typing import TYPE_CHECKING

from funpay.models import Lot
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class LotsHtmlParser(BaseHtmlParser):
    def _extract_offer_container(self, class_name: str) -> list['Tag']:
        return self.soup.find_all("div", {"class": class_name})

    def extract_game_id(self) -> str:
        content = self.soup.find("div", {"class": "page-content"})
        game_id = content.find("button")['data-game']

        return game_id

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
            title = offer_body.find("div", {"class": "tc-desc-text"}).text
            price = float(offer_body.find("div", {"class": "tc-price"})['data-s'])
            amount = offer_body.find("div", {"class": "tc-amount"})

            if amount:
                amount = int(amount.text)

            lots.append(Lot(
                node_id=node_id,
                title=title,
                price=price,
                amount=amount
            ))

        return lots
