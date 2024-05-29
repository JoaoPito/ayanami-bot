from app.app import AyanamiApp
from models.command_base import CommandBase
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

class PingCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app
        self.chat = app.chat

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and self.app.is_authorized(user.id):
            await self.chat.send_message(context=context, chat_id=update.effective_chat.id, text="pong")
        
    def create(self):
        return CommandHandler(self.name, self.handle)
    
class StartCommand(CommandBase):
    DEFAULT_MESSAGE = """🌟 Welcome, {user_name}! 🌟

Hi, I'm {bot_name}, your personal virtual assistant! 😜 I love anime and sci-fi movies. I'm here to help you with anything you need, whether it's a question or a curiosity.

Count on me for whatever you need! 
I just need you to use the '/auth' command followed by the access token, like this: '/auth 12345' so I can give full access to you!"""

    def __init__(self, name, app: AyanamiApp, message=DEFAULT_MESSAGE):
        super().__init__(name,)
        self.app = app
        self.chat = app.chat
        self.message = message

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        bot_name = await context.bot.getMyName()
        self.app.auth.register_new_user(user.id)
        if user != None:
            await self.chat.send_message(context=context, 
                                         chat_id=update.effective_chat.id, 
                                         text=self.message.format(user_name=user.first_name, bot_name=bot_name.name))
        
    def create(self):
        return CommandHandler(self.name, self.handle)