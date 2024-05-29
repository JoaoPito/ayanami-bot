from chat.chat_factory import ChatFactory
from chat.telegram.telegramchat import TelegramChat
from tests.chat.telegram.stubs import TelegramAppStub

class TelegramChatStubFactory(ChatFactory):
    def set_app_stub(self, stub):
        self.app_stub = stub

    def create(self):
        return TelegramChat(self.app_stub)