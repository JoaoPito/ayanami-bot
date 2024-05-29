from chat.telegram.commands.base import CommandBase
from telegram.ext import CommandHandler

class MessageCommandStub(CommandBase):
    has_called_handle = False

    def __init__(self, name, app):
        super().__init__(name)
        self.app = app

    async def handle(self, **kwargs):
        print("CALLED")
        self.has_called_handle = True

    def create(self):
        return CommandHandler(self.name, self.handle)