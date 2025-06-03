from typing import TYPE_CHECKING, Optional

from funpay.types import Message, Chat
from funpay.utils import string_to_datetime

from .base_html_parser import BaseHtmlParser

if TYPE_CHECKING:
    import datetime
    from bs4 import Tag
    from funpay.enums import Locale


class ChatParser(BaseHtmlParser):
    def _extract_chat_container(self) -> 'Tag':
        return self.soup.find("div", {"class": "chat chat-float"})

    def _parse_implementation(self, locale: 'Locale', since_date: Optional['datetime.datetime'] = None) -> 'Chat':
        chat_container = self._extract_chat_container()

        chat_id = int(chat_container["data-id"])
        interlocutor_id = int(chat_container["data-name"].split('-')[1])

        messages_soup = chat_container.find_all("div", {"class": "chat-msg-item chat-msg-with-head"})
        messages = []

        for message in messages_soup:
            message_id = int(message['id'].split('-')[1])
            content = self.get_text(message, "div.chat-msg-text")

            date = string_to_datetime(
                locale,
                message.find("div", {"class": "chat-msg-date"})['title']
            )

            if since_date and since_date < date:
                continue

            media_user_name = message.find("div", {"class": "media-user-name"})
            author_label = media_user_name.find("span", {"class": "chat-msg-author-label"})

            if author_label:
                continue

            else:
                author_link = media_user_name.find("a")
                author = author_link['href'].split('/')[-2]

            messages.append(
                Message(
                    id=message_id,
                    content=content,
                    date=date,
                    author_id=author,
                    chat_id=chat_id
                )
            )

        return Chat(
            id=chat_id,
            interlocutor_id=interlocutor_id,
            messages=messages
        )