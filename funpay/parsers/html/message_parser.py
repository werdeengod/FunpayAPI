from typing import TYPE_CHECKING, Optional

from funpay.types import Message
from funpay.utils import string_to_datetime

from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    import datetime
    from bs4 import Tag
    from funpay.enums import Locale


class MessageHtmlParser(BaseHtmlParser):
    """Parser for get message from link https://funpay.com/chat/?node={CHAT_ID}"""

    def _extract_message_container(self) -> 'Tag':
        return self.soup.find("div", {"class": "chat-msg-item"})

    def _parse_implementation(
        self,
        chat_id: int,
        locale: 'Locale',
        author_id: Optional[int] = None,
        date: Optional['datetime.datetime'] = None
    ) -> 'Message':

        message_container = self._extract_message_container()
        message_id = int(message_container['id'].split('-')[1])
        content = self.get_text(message_container, "div.chat-msg-text")

        chat_msg_date = message_container.find("div", {"class": "chat-msg-date"})

        if chat_msg_date:
            date = string_to_datetime(
                locale=locale,
                datetime_string=chat_msg_date['title']
            )

        media_user_name = message_container.find("div", {"class": "media-user-name"})

        if media_user_name:
            author_label = media_user_name.find("span", {"class": "chat-msg-author-label"})
            if author_label:
                return

            author_link = media_user_name.find("a")
            author_id = int(author_link['href'].split('/')[-2])

        return Message(
            id=message_id,
            content=content,
            date=date,
            author_id=author_id,
            chat_id=chat_id
        )