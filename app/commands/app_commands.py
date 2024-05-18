from app.app import AyanamiApp
from models.command_base import CommandBase
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

class PingCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and self.app.is_authorized(user.id):
            await self.chat.send_message(context=context, chat_id=update.effective_chat.id, text="pong")
        
    def create(self):
        return CommandHandler(self.name, self.handle)