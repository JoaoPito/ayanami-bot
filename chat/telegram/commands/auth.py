from auth.auth_interface import AuthInterface
from chat.chatbase import ChatBase
from chat.telegram.commands.base import CommandBase
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

class RegisterUserCommand(CommandBase):
    def __init__(self, name, auth: AuthInterface):
        super().__init__(name,)
        self.auth = auth

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        self.auth.register_new_user(user_id)

    def create(self):
        return CommandHandler(self.name, self.handle)

class TryAuthenticateUserCommand(CommandBase):
    def __init__(self, name, chat: ChatBase, auth: AuthInterface):
        super().__init__(name,)
        self.chat = chat
        self.auth = auth

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and not self.auth.is_authorized(user.id):
            input_token = context.args[0]
            try:
                self.auth.try_authorize_user(user.id, input_token)
                await self.chat.send_message(context=context, 
                                            chat_id=update.effective_chat.id,
                                            text="Registered! You can now send me messages.")
            except (AuthInterface.InvalidCriteriaError, AuthInterface.ForbiddenError) as exc:
                await self.chat.send_message(context=context, 
                                            chat_id=update.effective_chat.id,
                                            text=f"Error registering user\n\"{exc}\"")
        
    def create(self):
        return CommandHandler(self.name, self.handle)
