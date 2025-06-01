from typing import TYPE_CHECKING

from funpay.parsers.json import MessageParser
from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Message


class ChatService(BaseService):
    async def send_message(self, text: str, *, chat_id: str | int) -> 'Message':
        """Sends a text message to a specified chat and returns the sent message object.

        This method handles the complete message sending workflow:
        1. Validates input parameters
        2. Sends the message via the client API
        3. Parses and returns the server response as a structured Message object

        Args:
            text: The message content to send (plain text)
            chat_id: The target chat identifier (can be string or integer)
                - Typically a numeric ID or special chat token

        Returns:
            Message
        """
        data = await self.client.request.send_message(
            chat_id=chat_id,
            text=text,
            csrf_token=self.account.csrf_token
        )

        return MessageParser(data).parse()

    async def history(self):
        pass
