from typing import TYPE_CHECKING, Optional

from funpay.types import Lot, Node
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class LotHtmlParser(BaseHtmlParser):
    def _extract_offer_header(self) -> 'Tag':
        return self.soup.find("div", {"class": "offer-list-title-container"})

    def _extract_offer_body(self) -> 'Tag':
        return self.soup.find("a", {"class": "tc-item"})

    def _parse_implementation(self, **kwargs) -> 'Lot':
        offer_header = self._extract_offer_header()
        offer_body = self._extract_offer_body()

        if not offer_header or not offer_body:
            return

        node_link = offer_header.find("a")
        node = Node(
            id=int(node_link['href'].split('/')[-2]),
            name=node_link.text
        )

        lot_id = int(offer_body['href'].split('=')[1])
        title = self.get_text(offer_body, "div.tc-desc-text")
        price = float(offer_body.find("div", {"class": "tc-price"})['data-s'])
        amount = self.get_text(offer_body, "div.tc-amount", int)

        return Lot(
            id=lot_id,
            node=node,
            title=title,
            price=price,
            amount=amount
        )


class FunpayUserLotsHtmlParser(BaseHtmlParser):
    """Parser for get lots from link:
       - https://funpay.com/users/{USER_ID}/
    """

    def _extract_offer_container(self) -> list['Tag']:
        return self.soup.find_all("div", {"class": "offer"})

    def _parse_implementation(self, node_id: Optional[str] = None) -> list['Lot']:
        offers_soup = self._extract_offer_container()
        lots = []

        for offer in offers_soup:
            lot = LotHtmlParser(str(offer)).parse()

            if not lot or node_id and node_id != lot.node.id:
                continue

            lots.append(lot)

        return lots
