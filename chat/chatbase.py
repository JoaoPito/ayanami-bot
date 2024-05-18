from models.command_base import CommandBase

class ChatBase:
    def __init__(self):
        pass

    def add_handler(self, command: CommandBase):
        pass

    def run(self):
        pass

    def stop(self):
        pass

    async def send_message(self):
        pass