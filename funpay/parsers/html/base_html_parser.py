from typing import TYPE_CHECKING, Type, Any
from functools import cached_property

from bs4 import BeautifulSoup

from funpay.parsers import ABCParser

if TYPE_CHECKING:
    from bs4 import Tag


class BaseHtmlParser(ABCParser):
    """Base class for HTML document parsers using BeautifulSoup.

    Provides common HTML parsing functionality including:
    - BeautifulSoup document preparation
    - Helper methods for element selection
    - Cached document parsing

    Inherits:
        BaseParser: Abstract parser interface

    Args:
        html (str): Raw HTML content to parse

    Attributes:
        html (str): Original HTML content
    """
    def __init__(self, html: str):
        super().__init__(html)
        self.html = html

    @cached_property
    def soup(self) -> 'BeautifulSoup':
        """BeautifulSoup document representation (cached).

        Returns:
            BeautifulSoup: Parsed document tree
        """
        return BeautifulSoup(self.html, 'html.parser')

    @staticmethod
    def get_text(element: 'Tag', selector: str, to_type: Type[Any] = str) -> str:
        """Helper method to extract and clean text from HTML elements.

        Args:
            element (Tag): Parent BeautifulSoup Tag
            selector (str): CSS selector for target element
            to_type (Type[Any]): Type to convert the result to (default: str)

        Returns:
            str: Cleaned text content or None if element not found
        """
        if found := element.select_one(selector):
            return to_type(found.text.strip())

    def _parse_implementation(self, **kwargs) -> Any:
        raise NotImplementedError
