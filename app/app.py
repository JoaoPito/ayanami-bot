from auth.auth_interface import AuthInterface
from chat.message import ChatMessage
from ai.ai_interface import AIInterface
from chat.chatbase import ChatBase
from models.command_base import CommandBase

class AyanamiApp():
    ai: AIInterface|None = None
    chat: ChatBase|None = None

    def __init__(self, ai: AIInterface, chat: ChatBase, auth: AuthInterface|None):
        self.ai = ai
        self.chat = chat
        self.auth = auth

    def __message_handler__(self, message: ChatMessage):
        response = self.ai.invoke(message.content)
        self.chat.send(response)

    def __reset_handler__(self):
        self.ai.reset()

    def add_command_handler(self, command: CommandBase):
        self.chat.add_command_handler(command)

    def add_message_handler(self, command: CommandBase):
        self.chat.add_message_handler(command)

    def run(self):
        self.ai.run()
        self.chat.run()

    def is_authorized(self, user_id: int):
        return self.auth.is_authorized(user_id)
