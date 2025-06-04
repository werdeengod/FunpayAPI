from typing import TYPE_CHECKING

from funpay.types import Chat
from funpay.parsers.html import MessageHtmlParser

from .base_json_parser import BaseJsonParser

if TYPE_CHECKING:
    import datetime
    from funpay.enums import Locale


class ChatJsonParser(BaseJsonParser):
    """Parser for get chat from link https://fanpay.com/chat/history"""

    def _extract_node(self) -> dict:
        return self.data.get('node')

    def _extract_messages(self) -> dict:
        return self.data.get('messages')

    def _parse_implementation(self, locale: 'Locale', since_date: 'datetime.datetime') -> 'Chat':
        node = self._extract_node()

        if not node:
            return

        chat_id = node['id']
        interlocutor_id = int(node['name'].split('-')[1])

        messages_raw_list = self._extract_messages()
        last_author_id, last_date = None, None
        messages = []

        for raw_message in messages_raw_list:
            message = MessageHtmlParser(raw_message['html']).parse(
                chat_id=chat_id,
                locale=locale,
                author_id=last_author_id,
                date=last_date
            )

            if not message:
                continue

            last_date, last_author_id = message.date, message.author_id
            if since_date and since_date < message.date:
                continue

            messages.append(message)

        return Chat(
            id=chat_id,
            interlocutor_id=interlocutor_id,
            messages=messages
        )

