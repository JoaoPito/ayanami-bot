from chat.chatbase import ChatBase
from models.command_base import CommandBase

from telegram.ext import CommandHandler, MessageHandler, filters

class TelegramChat(ChatBase):
    def __init__(self, telegram_app):
        self.telegram_app = telegram_app
        return super().__init__()
    
    def add_command_handler(self, command: CommandBase):
        self.__add_handler__(command.name, command.handle)
        handler = CommandHandler(command.name, command.handle)
        self.telegram_app.add_handler(handler)

    def add_message_handler(self, command: CommandBase):
        self.__add_handler__(command.name, command.handle)
        self.telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), command.handle))

    def run(self):
        self.telegram_app.run_polling()