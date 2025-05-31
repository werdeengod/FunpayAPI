from typing import Any
from abc import ABC, abstractmethod
from functools import cached_property

from bs4 import BeautifulSoup


class BaseHtmlParser(ABC):
    def __init__(self, html: str):
        self.html = html

    @cached_property
    def soup(self) -> 'BeautifulSoup':
        return BeautifulSoup(self.html, 'html.parser')

    @abstractmethod
    def parse(self) -> Any:
        pass
