from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters
from app.app import AyanamiApp
from models.command_base import CommandBase

class MessageCommand(CommandBase):
    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ai_args = {"input": update.message.text}
        result = self.app.ai.invoke(ai_args)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result["output"])

    def create(self):
        return MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle)

class ResetCommand(CommandBase):
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='RESET')

    def create(self):
        return CommandHandler(self.name, self.handle)