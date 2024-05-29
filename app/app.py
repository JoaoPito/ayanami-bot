from auth.auth_interface import AuthInterface
from ai.ai_interface import AIInterface
from chat.chatbase import ChatBase
from chat.telegram.commands.base import CommandBase

class AyanamiApp():
    ai: AIInterface|None = None
    chat: ChatBase|None = None

    def __init__(self, ai: AIInterface, chat: ChatBase, auth: AuthInterface|None):
        self.ai = ai
        self.chat = chat
        self.auth = auth

    def __reset_handler__(self):
        self.ai.reset()

    def add_command(self, command: CommandBase):
        self.chat.add_handler(command)

    def run(self):
        self.ai.run()
        self.chat.run()

    def is_authorized(self, user_id: int):
        return self.auth.is_authorized(user_id)
