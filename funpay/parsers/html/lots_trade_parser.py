from .base_html_parser import BaseHtmlParser


class FunpayLotGameIdParser(BaseHtmlParser):
    def _extract_page_content(self):
        return self.soup.find("div", {"class": "page-content"})

    def parse(self) -> str:
        content = self._extract_page_content()
        game_id = content.find("button")['data-game']

        return game_id
