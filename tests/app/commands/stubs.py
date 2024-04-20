from models.command_base import CommandBase

class MessageCommandStub(CommandBase):
    has_called_handle = False

    async def handle(self, **kwargs):
        self.has_called_handle = True