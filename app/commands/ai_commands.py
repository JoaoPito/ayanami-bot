from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters
from app.app import AyanamiApp
from chat.multimedia.files import download_file_from_id
from chat.multimedia.images import load_using_base64
from models.command_base import CommandBase

class MessageCommand(CommandBase):
    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app
        self.chat = app.chat

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and self.app.is_authorized(user.id):
            ai_args = {"input_text": update.message.text, "username": update.message.from_user.first_name}
            result = self.app.ai.invoke(ai_args)
            await self.chat.send_message(context=context, chat_id=update.effective_chat.id, text=result["output"])

    def create(self):
        return MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle)
    
class ImageCommand(CommandBase):
    IMAGE_FILEPATH = "./downloaded/photos/"

    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app
        self.chat = app.chat

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and self.app.is_authorized(user.id):
            image_url = await self.__download_image_from_chat__(update.message, context.bot)
            base64_image = load_using_base64(image_url)
            text = update.message.caption

            ai_args = {"input_text": text, "input_image": base64_image, "username": update.message.from_user.first_name}
            result = self.app.ai.invoke(ai_args)
            await self.chat.send_message(context=context, chat_id=update.effective_chat.id, text=result["output"])

    async def __download_image_from_chat__(self, message, bot):
        file_id = message.photo[-1].file_id
        path = await download_file_from_id(bot, file_id, self.IMAGE_FILEPATH)
        return path

    def create(self):
        return MessageHandler(filters.PHOTO & (~filters.COMMAND), self.handle)

class ResetCommand(CommandBase):
    def __init__(self, name, app: AyanamiApp):
        super().__init__(name,)
        self.app = app
        self.chat = app.chat

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and self.app.is_authorized(user.id):
            self.app.ai.reset_history()
            await self.chat.send_message(context=context, chat_id=update.effective_chat.id, text="Ok!")

    def create(self):
        return CommandHandler(self.name, self.handle)
    
class ChangeAICommand(CommandBase):
    def __init__(self, name, app: AyanamiApp, config):
        super().__init__(name,)
        self.app = app
        self.chat = app.chat
        self.available_ai = config

    def __get_params_from_args__(self, args):
        model = args[0].lower()
        temp = 0
        system = ''
        self.app.ai.set_ai_model(self.available_ai[model])
        if len(args) > 1:
            temp = float(args[1])
            self.app.ai.set_ai_temp(temp)
        if len(args) > 2:
            system = args[2]
            self.app.ai.set_ai_system(system)
        return model, temp, system

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        if user != None and self.app.is_authorized(user.id):
            args = context.args
            model, temp, system = self.__get_params_from_args__(args)
            try:
                await self.chat.send_message(context=context, 
                                            chat_id=update.effective_chat.id,
                                            text=f"Updated AI with model '{self.available_ai[model]}', temp {temp} and system prompt '{system}'")
            except Exception as exc:
                await self.chat.send_message(context=context, 
                                            chat_id=update.effective_chat.id,
                                            text=f"Error setting AI parameters. Are your arguments correct?")
                raise exc

    def create(self):
        return CommandHandler(self.name, self.handle)