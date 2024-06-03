from core.chat.chat_factory import ChatFactory
from core.chat.chatinterface import ChatInterface
from chat.telegram.telegramchat import TelegramChat

from telegram.ext import ApplicationBuilder

class TelegramChatFactory(ChatFactory):
    def create(self, token: str) -> ChatInterface:
        tel_application = ApplicationBuilder().token(token).build()
        return TelegramChat(tel_application)