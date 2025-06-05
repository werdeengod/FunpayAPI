from typing import TYPE_CHECKING
import json

from funpay.types import Game, Node, Account
from funpay.enums import Locale

from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class FunpayGamesHtmlParser(BaseHtmlParser):
    """Parser for get all games from link:
       - https://funpay.com/
    """

    def _extract_promo_game_list(self) -> 'Tag':
        return self.soup.find("div", {"class": "promo-game-list"})

    def _parse_implementation(self) -> list['Game']:
        promo_game_list = self._extract_promo_game_list()
        promo_game_items = promo_game_list.find_all("div", {"class": "promo-game-item"})
        games = []

        for game in promo_game_items:
            game_data = game.find("div", {"class": "game-title"})

            game_id = game_data['data-id']
            game_name = game_data.text.strip()

            ul = game.find("ul")
            list_nodes = ul.find_all("li")
            nodes = []

            for node in list_nodes:
                link = node.find("a")

                node_id = link['href'].split('/')[-2]
                node_name = link.text

                nodes.append(
                    Node(
                        id=int(node_id),
                        name=node_name
                    )
                )

            games.append(
                Game(
                    id=game_id,
                    name=game_name,
                    nodes=nodes
                )
            )

        return games


class FunpayAccountHtmlParser(BaseHtmlParser):
    """Parser for get account data from link:
       - https://funpay.com/
    """

    def _extract_account_data(self) -> dict:
        return json.loads(self.soup.find("body")["data-app-data"])

    def _extract_account_username(self) -> str:
        return self.get_text(self.soup, "div.user-link-name")

    def _extract_balance(self) -> int | None:
        balance = self.get_text(self.soup, "span.badge.badge-balance", to_type=int)
        return balance

    def _parse_implementation(self) -> 'Account':
        data = self._extract_account_data()
        locale = Locale(data['locale'])

        return Account(
            id=int(data['userId']),
            csrf_token=data['csrf-token'],
            username=self._extract_account_username(),
            balance=self._extract_balance(),
            locale=locale
        )


