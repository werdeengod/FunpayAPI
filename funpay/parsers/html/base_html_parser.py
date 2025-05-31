from typing import TYPE_CHECKING, Type, Any
from functools import cached_property

from bs4 import BeautifulSoup

from funpay.parsers import BaseParser

if TYPE_CHECKING:
    from bs4 import Tag


class BaseHtmlParser(BaseParser):
    def __init__(self, html: str):
        self.html = html

    @cached_property
    def soup(self) -> 'BeautifulSoup':
        return BeautifulSoup(self.html, 'html.parser')

    @staticmethod
    def get_text(element: 'Tag', selector: str, to_type: Type[Any] = str) -> str:
        if found := element.select_one(selector):
            return to_type(found.text.strip())

    def parse(self) -> Any:
        raise NotImplementedError
