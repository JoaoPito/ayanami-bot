from app.app import AyanamiApp
from auth.auth_interface import AuthInterface
from chat.telegram.commands.base import CommandBase
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

class RegisterUserCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        self.app.auth.register_new_user(user_id)

    def create(self):
        return CommandHandler(self.name, self.handle)

class TryAuthenticateUserCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app
        self.chat = app.chat

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and not self.app.is_authorized(user.id):
            input_token = context.args[0]
            try:
                self.app.auth.try_authorize_user(user.id, input_token)
                await self.chat.send_message(context=context, 
                                            chat_id=update.effective_chat.id,
                                            text="Ok!")
            except (AuthInterface.InvalidCriteriaError, AuthInterface.ForbiddenError) as exc:
                await self.chat.send_message(context=context, 
                                            chat_id=update.effective_chat.id,
                                            text=f"Error registering user\n\"{exc}\"")
        
    def create(self):
        return CommandHandler(self.name, self.handle)
