from typing import TYPE_CHECKING, Optional

from funpay.parsers.json import RunnerMessageJsonParser, ChatJsonParser
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

        Note:
            - Automatically includes required CSRF token from account
            - Message content should be plain text (no HTML formatting)
        """
        data = await self.client.request.send_message(
            chat_id=chat_id,
            text=text,
            csrf_token=self._account.csrf_token
        )

        message = RunnerMessageJsonParser(data).parse(
            locale=self._account.locale,
            author_id=self._account.id
        )

        return message

    async def get_history(
        self,
        chat_id: int,
        *,
        last_message_id: Optional[int] = 99999999999999999,
        since_date: Optional['datetime.datetime'] = None
    ) -> 'Chat':
        """Retrieves chat message history with optional date filtering.

        Args:
            chat_id: Numeric identifier of the target chat
            since_date: Optional cutoff date for historical messages
                - When provided, only returns messages newer than this date
                - When None, returns full available history
            last_message_id: ID of the message from which to start the history (FunPay filter).

        Returns:
            Chat: Complete chat object with messages and metadata

        Raises:
            HttpRequestError: For API communication failures (status >= 400)
            ParserError: When critical HTML parsing fails

        Note:
            - Results are parsed according to account's locale settings
            - Pagination is handled automatically by the client
        """
        data = await self.client.request.fetch_chat_history(
            chat_id=chat_id,
            last_message=last_message_id
        )

        if not data:
            return

        chat = ChatJsonParser(data).parse(
            locale=self._account.locale,
            since_date=since_date
        )

        return chat

