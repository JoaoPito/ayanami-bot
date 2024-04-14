import unittest
from app.app_builder import AyanamiAppBuilder, error_not_assigned_message, param_names

from tests.chat.stubs import EmptyChatStub
from tests.ai.stubs import EmptyAIStub
from tests.auth.stubs import EmptyAuthStub

from app.app import AyanamiApp

class AppBuilderTester(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = AyanamiAppBuilder()

    def test_if_is_adding_chat_correctly(self):
        chat = EmptyChatStub()
        self.builder.set_chat(chat)
        self.assertEqual(self.builder.chat, chat, "Builder did not add Chat as expected")

    def test_if_is_adding_ai_correctly(self):
        ai = EmptyAIStub()
        self.builder.set_ai(ai)
        self.assertEqual(self.builder.ai, ai, "Builder did not add AI as expected")

    def test_if_is_adding_auth_correctly(self):
        auth = EmptyAuthStub()
        self.builder.set_authenticator(auth)
        self.assertEqual(self.builder.auth, auth, "Builder did not add authenticator as expected")

    def test_if_is_building_app_with_all_params(self):
        ai = EmptyAIStub()
        chat = EmptyChatStub()
        auth = EmptyAuthStub()
        expected_app = AyanamiApp(ai, chat, auth)

        builder = AyanamiAppBuilder()
        builder.set_ai(ai)
        builder.set_chat(chat)
        builder.set_authenticator(auth)
        result_app = builder.build_app()

        self.assertEqual(result_app.ai, expected_app.ai, "Builder did not initialize ai to app as expected")
        self.assertEqual(result_app.chat, expected_app.chat, "Builder did not initialize chat to app as expected")
        self.assertEqual(result_app.auth, expected_app.auth, "Builder did not initialize auth to app as expected")

    def __test_if_raises_correct_exception__(self, exc_class, message, function):
        try:
            function()
        except exc_class as exc:
            self.assertEqual(str(exc), message, "Exception message was not correctly set")
            return
        except:
            self.fail("Builder did not raise correct exception")
        self.fail("Builder did not raise any exceptions") 

    def test_if_raises_error_building_without_ai_param(self):
        chat = EmptyChatStub()
        auth = EmptyAuthStub()
        expected_message = error_not_assigned_message.format(param=param_names['AI'])

        builder = AyanamiAppBuilder()
        builder.set_chat(chat)
        builder.set_authenticator(auth)

        self.__test_if_raises_correct_exception__(TypeError, expected_message, builder.build_app)

    def test_if_raises_error_building_without_chat_param(self):
        ai = EmptyAIStub()
        auth = EmptyAuthStub()
        expected_message = error_not_assigned_message.format(param=param_names['Chat'])

        builder = AyanamiAppBuilder()
        builder.set_ai(ai)
        builder.set_authenticator(auth)

        self.__test_if_raises_correct_exception__(TypeError, expected_message, builder.build_app)
    
    def test_if_is_building_without_auth_param(self):
        ai = EmptyAIStub()
        chat = EmptyChatStub()

        builder = AyanamiAppBuilder()
        builder.set_ai(ai)
        builder.set_chat(chat)
        app = builder.build_app()

        self.assertIsInstance(app, AyanamiApp, "Builder did not return correct class instance")
        self.assertEqual(app.chat, chat, "Builder did not initialize correct chat param")
        self.assertEqual(app.ai, ai, "Builder did not initialize correct ai param")
        self.assertEqual(app.auth, None, "Builder did not initialize app with empty authorization")
