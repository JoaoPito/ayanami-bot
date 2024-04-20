import asyncio
from chat.chatbase import ChatBase

class EmptyChatStub(ChatBase):
    filters = {"message": "msg"}
    has_called_add_handler = False
    has_run = False
    
    def __init__(self):
        pass

    def add_handler(self, name: str, handler):
        self.has_called_add_handler = True
        return super().add_handler(name, handler)
    
    def run(self):
        self.has_run = True

    def call_handler(self, name, **kwargs):
        asyncio.run(self.handlers[name](**kwargs))
