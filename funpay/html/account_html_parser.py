import json

from funpay.models import Account, Review, Lot
from .base_html_parser import BaseHtmlParser


class AccountHtmlParser(BaseHtmlParser):
    def _extract_account_data(self) -> dict:
        return json.loads(self.soup.find("body")["data-app-data"])

    def _extract_account_username(self) -> str:
        return self.soup.find("div", {"class": "user-link-name"}).text

    def _extract_balance(self) -> int | None:
        balance = self.soup.find("span", {"class": "badge badge-balance"})

        if balance:
            balance = int(balance.text.replace(' ₽', ''))

        return balance

    def parse(self) -> 'Account':
        data = self._extract_account_data()

        return Account(
            id=int(data['userId']),
            csrf_token=data['csrf-token'],
            username=self._extract_account_username(),
            balance=self._extract_balance()
        )
