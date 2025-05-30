from abc import ABC
from bs4 import BeautifulSoup


class BaseParser(ABC):
    def __init__(self, html: str):
        self.html = html

    @property
    def soup(self) -> 'BeautifulSoup':
        return BeautifulSoup(self.html, 'html.parser')
