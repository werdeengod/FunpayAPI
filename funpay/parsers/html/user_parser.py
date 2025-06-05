from typing import TYPE_CHECKING
from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    from bs4 import Tag


class FunpayUserProfileHtmlParser(BaseHtmlParser):
    """Parser for get profile from link https://funpay.com/users/{USER_ID}/"""
    pass


