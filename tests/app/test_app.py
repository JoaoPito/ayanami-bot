import unittest

from app.app import AyanamiApp
from tests.ai.stubs import EmptyAIStub
from tests.app.commands.stubs import MessageCommandStub
from tests.auth.stubs import EmptyAuthStub
from tests.chat.stubs import EmptyChatStub

class AppTester(unittest.TestCase):
    def __create_command_stub__(self):
        return MessageCommandStub(self.chat.filters['message'], self.app)

    def setUp(self) -> None:
        self.ai = EmptyAIStub()
        self.chat = EmptyChatStub()
        self.auth = EmptyAuthStub()
        self.app = AyanamiApp(self.ai, self.chat, self.auth)

    def test_is_adding_handler_to_chat(self):
        command = self.__create_command_stub__()
        self.app.add_command(command)
        self.assertTrue(self.chat.has_called_add_handler)

    def test_if_is_assigning_command_names(self):
        command = self.__create_command_stub__()
        self.app.add_command(command)
        self.assertIn(command.name, self.chat.handlers)

    def test_if_is_assigning_command_handlers(self):
        command = self.__create_command_stub__()
        self.app.add_command(command)
        self.assertEqual(command.handle, self.chat.handlers[command.name])

    def test_if_runs_chat_when_called_run(self):
        self.app.run()
        self.assertTrue(self.chat.has_run)
    
    def test_if_runs_ai_when_called_run(self):
        self.app.run()
        self.assertTrue(self.ai.has_run)

    def test_authorization(self):
        self.auth.is_permissive = True
        self.assertTrue(self.app.is_authorized(696969), "App did not authorize access.")

        self.auth.is_permissive = False
        self.assertFalse(self.app.is_authorized( 696969), "App authorized access when should not.")
