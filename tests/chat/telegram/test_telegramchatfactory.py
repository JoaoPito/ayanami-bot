import unittest

from chat.telegram.telegramchat import TelegramChat
from chat.telegram.telegramchat_factory import TelegramChatFactory

class TestTelegramChatFactory(unittest.TestCase):
    def test_if_return_correct_obj(self):
        factory = TelegramChatFactory()
        self.assertIsInstance(factory.create(token='abc'), 
                              TelegramChat, 
                              "Factory did not return correct TelegramChat instance")