from .base import BaseService


class ChatService(BaseService):
    async def send_message(self, chat_id: str | int, text: str):
        pass

    async def history(self):
        pass
