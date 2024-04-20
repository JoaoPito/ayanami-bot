from auth.auth_interface import AuthInterface
from chat.message import ChatMessage
from ai.ai_interface import AIInterface
from chat.chat_interface import ChatInterface

class AyanamiApp():
    ai: AIInterface|None = None
    chat: ChatInterface|None = None

    def __init__(self, ai: AIInterface, chat: ChatInterface, auth: AuthInterface|None):
        self.ai = ai
        self.chat = chat
        self.auth = auth

    def __message_handler__(self, message: ChatMessage):
        response = self.ai.invoke(message.content)
        self.chat.send(response)

    def __reset_handler__(self):
        self.ai.reset()

    def add_command(self, command):
        self.chat.add_handler(command.name, command.handle)

    def run(self):
        self.ai.run()
        self.chat.run()
