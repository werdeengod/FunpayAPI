from typing import TYPE_CHECKING

from funpay.enums import Locale, OrderType
from funpay.types import Order, OrderCut, UserCut, Node
from funpay.utils import string_to_datetime, get_order_status_from_string

from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class FunpayOrderHtmlParser(BaseHtmlParser):
    """Parser for get order from links:
       - https://funpay.com/orders/{ORDER_CODE}/
    """
    def _extract_page_content(self):
        return self.soup.find("div", {"class": "page-content"})

    def _extract_media_user_name(self) -> 'Tag':
        return self.soup.find("div", {"class": "media-user-name"})

    def _parse_implementation(self, locale: 'Locale') -> 'Order':
        page_content = self._extract_page_content()
        header_data = self.get_text(page_content, "h1.page-header.page-header-no-hr.page-header-params").split()

        if len(header_data) != 3:
            return

        order_code = header_data[1][1:]
        status = get_order_status_from_string(
            locale=locale,
            status_string=header_data[2]
        )

        node_link = page_content.find("a")

        node = Node(
            id=node_link['href'].split('/')[-2],
            name=node_link.text
        )

        if locale == Locale.RU:
            title_search = "Краткое описание"
            description_search = "Подробное описание"
            start_date_search = "Открыт"
            end_date_search = "Закрыт"
            amount_search = "Сумма"

        else:
            title_search = "Short description"
            description_search = "Detailed description"
            start_date_search = "Open"
            end_date_search = "Closed"
            amount_search = "Total"

        title = self.soup.find(
            "h5",
            text=title_search
        ).find_next('div').text.strip()

        description = self.soup.find("h5", text=description_search).find_next('div').text.strip()

        start_date_text = self.soup.find("h5", text=start_date_search).find_next('div').text.split('(')[0].strip()
        start_date = string_to_datetime(
            locale=locale,
            datetime_string=start_date_text
        )

        end_date_text = self.soup.find("h5", text=end_date_search).find_next('div').text.split('(')[0].strip()
        end_date = string_to_datetime(
            locale=locale,
            datetime_string=end_date_text
        )

        price = float(self.soup.find("h5", text=amount_search).find_next('div').text.split()[0])

        media_user_name = self._extract_media_user_name()
        user_data = media_user_name.find("a")

        user = UserCut(
            id=int(user_data['href'].split('/')[-2]),
            username=user_data.text.strip()
        )

        return Order(
            id=order_code,
            status=status,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            price=price,
            node=node,
            order_type=None,
            user=user
        )


class OrderCutHtmlParser(BaseHtmlParser):
    def _extract_media_user_name(self) -> 'Tag':
        return self.soup.find("div", {"class": "media-user-name"})

    def _parse_implementation(self, locale: 'Locale', order_type: 'OrderType') -> 'OrderCut':
        datetime_string = self.get_text(self.soup, "div.tc-date-time")
        date = string_to_datetime(
            locale=locale,
            datetime_string=datetime_string
        )

        order_code = self.get_text(self.soup, "div.tc-order")
        title = self.get_text(self.soup, "div.order-desc > div:first-child")

        media_user_name = self._extract_media_user_name()
        user_data = media_user_name.find("span", {"class": "pseudo-a"})

        user = UserCut(
            id=int(user_data['data-href'].split('/')[-2]),
            username=user_data.text.strip()
        )

        status = get_order_status_from_string(
            locale=locale,
            status_string=self.get_text(self.soup, "div.tc-status")
        )

        price = float(self.get_text(self.soup, "div.tc-price").split()[0])

        return OrderCut(
            id=order_code,
            start_date=date,
            title=title,
            user=user,
            status=status,
            price=price,
            order_type=order_type
        )


class FunpayOrdersCutHtmlParser(BaseHtmlParser):
    """Parser for get orders from links:
       - https://funpay.com/orders/trade
       - https://funpay.com/orders/
    """
    def _extract_orders(self) -> list['Tag']:
        return self.soup.find_all("a", {"class": "tc-item"})

    def _parse_implementation(self, locale: 'Locale', order_type: 'OrderType') -> list['OrderCut']:
        orders_soup = self._extract_orders()

        orders = [
            OrderCutHtmlParser(str(order_soup)).parse(
                locale=locale,
                order_type=order_type
            )
            for order_soup in orders_soup
        ]

        return orders
