from models.command_base import CommandBase

class ChatBase:
    filters = {}
    handlers = {}

    def __init__(self):
        pass

    def __add_handler__(self, name, handler):
        self.handlers[name] = handler

    def add_command_handler(self, command: CommandBase):
        self.__add_handler__(command.name, command.handle)

    def add_message_handler(self, command: CommandBase):
        self.__add_handler__(command.name, command.handle)

    def run(self):
        pass

    def stop(self):
        pass