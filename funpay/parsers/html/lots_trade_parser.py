from funpay.types import Node
from .base_html_parser import BaseHtmlParser


class FunpayLotGameIdParser(BaseHtmlParser):
    def _extract_page_content(self):
        return self.soup.find("div", {"class": "page-content"})

    def _parse_implementation(self) -> str:
        content = self._extract_page_content()
        game_id = content.find("button")['data-game']

        return game_id


class FunpayLotNodeParser(BaseHtmlParser):
    def _extract_back_link(self):
        return self.soup.find("div", {"class": "back-link"})

    def _parse_implementation(self) -> 'Node':
        back_link = self._extract_back_link()

        node_id = back_link.find("a")['href'].split('/')[-2]
        node_name = self.get_text(back_link, "span.inside")

        return Node(
            id=node_id,
            name=node_name
        )