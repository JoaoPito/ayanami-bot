from ai.ai_interface import AIInterface
from chat.chat_interface import ChatInterface

class CommandBase:
    def __init__(self, chat: ChatInterface, ai: AIInterface):
        self.chat = chat
        self.ai = ai

    def handle(self, **kwargs):
        pass
