from telegram import Update, constants
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters
from app.app import AyanamiApp
from models.command_base import CommandBase

class MessageCommand(CommandBase):
    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ai_args = {"input": update.message.text, "username": update.message.from_user.first_name}
        result = self.app.ai.invoke(ai_args)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=result["output"], 
                                       connect_timeout=60)

    def create(self):
        return MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle)

class ResetCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.app.ai.reset_history()
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="Ok!", 
                                       connect_timeout=60)

    def create(self):
        return CommandHandler(self.name, self.handle)
    
class PingCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="pong", 
                                       connect_timeout=60)

    def create(self):
        return CommandHandler(self.name, self.handle)