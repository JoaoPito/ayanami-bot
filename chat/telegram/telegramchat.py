from core.chat.chatinterface import ChatInterface
from chat.telegram.multimedia.text import split_phrases
from chat.telegram.commands.base import CommandBase
from telegram.ext import Application

class TelegramChat(ChatInterface):
    def __init__(self, telegram_app: Application):
        self.app = telegram_app
        return super().__init__()

    def add_command(self, command: CommandBase):
        self.app.add_handler(command.create())

    def run(self):
        self.app.run_polling()

    def stop(self):
        self.app.stop_running()

    async def send_message(self, context, chat_id, text, connect_timeout=60, max_chars=4096):
        text_pieces = split_phrases(text, max_chars=max_chars)
        for piece in text_pieces:
            await context.bot.send_message(chat_id=chat_id, 
                                            text=piece, 
                                            connect_timeout=connect_timeout)