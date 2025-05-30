import json

from funpay.models import Account, Review, Lot
from .base_parser import BaseParser


class AccountParser(BaseParser):
    def get(self) -> 'Account':
        data = json.loads(self.soup.find("body")["data-app-data"])
        username = self.soup.find("div", {"class": "user-link-name"}).text
        balance = self.soup.find("span", {"class": "badge badge-balance"})

        if balance:
            balance = int(balance.text.replace(' ₽', ''))

        return Account(
            id=int(data['userId']),
            csrf_token=data['csrf-token'],
            username=username,
            balance=balance
        )

    def reviews(self) -> list['Review']:
        review_containers = self.soup.find_all("div", {"class": "review-container"})
        reviews = []

        for review in review_containers:
            username = review.find("div", {"class": "media-user-name"}).text
            order_code = review.find("div", {"class": "review-item-order"}).text
            date = review.find("div", {"class": "review-item-date"}).text
            text = review.find("div", {"class": "review-item-text"}).text.strip()

            reviews.append(Review(
                username=username,
                order_code=order_code,
                date=date,
                text=text
            ))

        return reviews

    def lots(self) -> list['Lot']:
        offers_soup = self.soup.find_all("div", {"class": "offer"})
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
