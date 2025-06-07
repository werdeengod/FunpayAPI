from typing import TYPE_CHECKING

from funpay.enums import OrderType
from funpay.parsers.html import FunpayOrdersCutHtmlParser, FunpayOrderHtmlParser
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Order, OrderCut


class OrdersService(BaseService):
    """Service for managing order operations and transaction handling.

    Provides functionality to:
    - Retrieve sales and purchase order lists
    - Get detailed information about specific orders
    - Process order refunds and cancellations
    - Handle order-related operations through the platform API
    """
    async def sales(self) -> list['OrderCut']:
        """Retrieves a list of the user's sales orders from FunPay.

        Returns:
            list[OrderCut]: A list of simplified order objects representing sales.
        """
        html = await self.client.request.fetch_sales_page()

        orders = FunpayOrdersCutHtmlParser(html).parse(
            locale=self._account.locale,
            order_type=OrderType.SALE
        )

        return orders

    async def purchases(self) -> list['OrderCut']:
        """Retrieves a list of the user's purchase orders from FunPay.

        Returns:
            list[OrderCut]: A list of simplified order objects representing purchases.
        """
        html = await self.client.request.fetch_purchases_page()

        orders = FunpayOrdersCutHtmlParser(html).parse(
            locale=self._account.locale,
            order_type=OrderType.PURCHASE
        )

        return orders

    async def get(self, order_code: str) -> 'Order':
        """Retrieves detailed information about a specific order.

        Args:
            order_code: The unique identifier of the order.

        Returns:
            Order: A complete order object with all available details.
        """
        html = await self.client.request.fetch_order_page(order_code)
        order = FunpayOrderHtmlParser(html).parse(locale=self._account.locale)
        return order

    async def refund(self, order_code: str) -> None:
        """Initiates a refund process for the specified order.

        Args:
            order_code: The unique identifier of the order to refund.

        Raises:
            HttpRequestError: If the refund request fails on server side.

        Note:
            Requires a valid CSRF token from the active session.
        """
        await self.client.request.send_refund(
            order_code=order_code,
            csrf_token=self._account.csrf_token
        )
