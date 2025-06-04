import datetime

from funpay.types import Message
from funpay.parsers.html import MessageHtmlParser
from funpay.enums import Locale

from .base_json_parser import BaseJsonParser


class RunnerMessageJsonParser(BaseJsonParser):
    """Parser for get message from link https://funpay.com/runner/"""

    def _parse_implementation(self, locale: 'Locale', author_id: int) -> 'Message':
        objects = self.data.get('objects')

        if not objects:
            return

        def _get_data_from_object() -> dict:
            for obj in objects:
                if obj.get('type') == 'chat_node':
                    return obj.get('data')

        data = _get_data_from_object()

        chat_id = data['node']['id']
        last_message = data['messages'][-1]

        return MessageHtmlParser(last_message['html']).parse(
            chat_id=chat_id,
            locale=locale,
            date=datetime.datetime.now(tz=datetime.timezone.utc),
            author_id=author_id
        )