from typing import TYPE_CHECKING, Optional

from funpay.parsers.json import MessageParser
from funpay.parsers.html import ChatParser

from .base import BaseService

if TYPE_CHECKING:
    from funpay.types import Message, Chat
    import datetime


class ChatService(BaseService):
    """Service for managing chat operations and message handling.

    Provides functionality to:
    - Send text messages to specific chats
    - Retrieve chat message history
    - Handle chat-related operations through the platform API
    """
    async def send_message(self, text: str, *, chat_id: str | int) -> 'Message':
        """Sends a text message to the specified chat.

        Args:
            text: The plain text content of the message to send
            chat_id: Unique identifier of the target chat (string or integer format)

        Returns:
            Message: The sent message object with all server-populated fields

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Workflow:
            1. Validates input parameters
            2. Submits message through client API
            3. Parses server response into Message object
            4. Returns structured message data

        Note:
            - Automatically includes required CSRF token from account
            - Message content should be plain text (no HTML formatting)
        """
        data = await self._client.request.send_message(
            chat_id=chat_id,
            text=text,
            csrf_token=self._account.csrf_token
        )

        return MessageParser(data).parse()

    async def history(self, chat_id: int, *, since_date: Optional['datetime.datetime'] = None) -> 'Chat':
        """Retrieves chat message history with optional date filtering.

        Args:
            chat_id: Numeric identifier of the target chat
            since_date: Optional cutoff date for historical messages
                - When provided, only returns messages newer than this date
                - When None, returns full available history

        Returns:
            Chat: Complete chat object with messages and metadata

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            - Results are parsed according to account's locale settings
            - Pagination is handled automatically by the client
        """
        html = await self._client.request.fetch_chat_page(chat_id=chat_id)

        chat = ChatParser(html).parse(
            locale=self._account.locale,
            since_date=since_date
        )

        return chat

