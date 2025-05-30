from .base_parser import BaseParser


class LotParser(BaseParser):
    def get_game_id(self) -> str:
        content = self.soup.find("div", {"class": "page-content"})
        game_id = content.find("button")['data-game']

        return game_id

    def get_nodes_id(self) -> list[str]:
        offers_soup = self.soup.find_all("div", {"class": "offer-list-title-container"})
        nodes = []

        for offer in offers_soup:
            category_id = offer.find("a")['href'].split('/')[-2]
            nodes.append(category_id)

        return nodes
