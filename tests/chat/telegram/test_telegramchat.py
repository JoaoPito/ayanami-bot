import unittest

from chat.telegram.telegramchat import TelegramChat
from tests.app.stubs import EmptyAppStub
from tests.chat.telegram.stubs import TelegramAppStub
from tests.models.command_stubs import MessageCommandStub

from telegram.ext import filters

STUB_FILTERS = "stub"

class TestTelegramChat(unittest.TestCase):
    def setUp(self) -> None:
        self.telegram_app = TelegramAppStub()
        self.chat = TelegramChat(self.telegram_app)

    def __build_command_stub__(self):
        self.app = EmptyAppStub()
        return MessageCommandStub(STUB_FILTERS, self.app)

    def test_if_assigns_handlers_correctly(self):
        command = self.__build_command_stub__()
        self.chat.add_command(command)
        handlers_callbacks = list(map(lambda k: self.telegram_app.handlers_added[k].callback, list(self.telegram_app.handlers_added)))
        self.assertIn(command.handle, handlers_callbacks)

    def test_if_calls_commands_when_receives_msg(self):
        pass
        #command = self.__build_command_stub__()
        #self.chat.add_command_handler(command)

        #self.telegram_app.call_handler(STUB_FILTERS)

        #self.assertTrue(command.has_called_handle)

    def test_if_call_message_handler_when_receives_msg(self):
        pass
    
    def test_if_answers_to_user_correctly(self):
        pass
    
    def test_if_runs_telegram(self):
        self.chat.run()
        self.assertTrue(self.telegram_app.is_running)