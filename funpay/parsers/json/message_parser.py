from funpay.types import Message
from .base_json_parser import BaseJsonParser


class MessageParser(BaseJsonParser):
    def parse(self) -> 'Message':
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
        author_id = last_message['author']
        message_id = last_message['id']
        content = last_message['content']

        return Message(
            id=message_id,
            chat_id=chat_id,
            content=content,
            author_id=author_id
        )


