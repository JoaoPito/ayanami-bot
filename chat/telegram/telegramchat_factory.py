from chat.chat_factory import ChatFactory
from chat.chatbase import ChatBase
from chat.telegram.telegramchat import TelegramChat

from telegram.ext import ApplicationBuilder

class TelegramChatFactory(ChatFactory):
    def create(self, token: str) -> ChatBase:
        tel_application = ApplicationBuilder().token(token).build()
        return TelegramChat(tel_application)