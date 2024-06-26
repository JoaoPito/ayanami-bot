import asyncio
from chat.chatbase import ChatBase
from chat.telegram.commands.base import CommandBase

class EmptyChatStub(ChatBase):
    filters = {"message": "msg"}
    has_called_add_handler = False
    has_run = False

    handlers = {}
    
    def __init__(self):
        pass

    def add_handler(self, command: CommandBase):
        self.has_called_add_handler = True
        self.handlers[command.name] = command.handle
    
    def run(self):
        self.has_run = True

    def call_handler(self, name, **kwargs):
        asyncio.run(self.handlers[name](**kwargs))
