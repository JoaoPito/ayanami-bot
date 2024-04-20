from telegram import Update
from telegram.ext import ContextTypes
from app.app import AyanamiApp
from models.command_base import CommandBase

class MessageCommand(CommandBase):
    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(context)
        text_caps = update.message.text.upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

class ResetCommand(CommandBase):
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='RESET')