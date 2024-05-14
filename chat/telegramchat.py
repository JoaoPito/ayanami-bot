from chat.chatbase import ChatBase
from models.command_base import CommandBase

from telegram.ext import CommandHandler, MessageHandler, filters

class TelegramChat(ChatBase):
    def __init__(self, telegram_app):
        self.telegram_app = telegram_app
        return super().__init__()

    def add_handler(self, command: CommandBase):
        self.telegram_app.add_handler(command.create())

    def run(self):
        self.telegram_app.run_polling()

    async def send_message(self, context, chat_id, text, connect_timeout=60):
        await context.bot.send_message(chat_id=chat_id, 
                                       text=text, 
                                       connect_timeout=connect_timeout)