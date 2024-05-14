import datetime
import os
from telegram import Update, constants
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters
from app.app import AyanamiApp
from models.command_base import CommandBase
import base64

class MessageCommand(CommandBase):
    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ai_args = {"input_text": update.message.text, "username": update.message.from_user.first_name}
        result = self.app.ai.invoke(ai_args)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=result["output"], 
                                       connect_timeout=60)

    def create(self):
        return MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle)
    
class ImageCommand(CommandBase):
    IMAGE_FILEPATH = "./downloaded/photos/"

    def __init__(self, app: AyanamiApp):
        super().__init__("msg",)
        self.app = app

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        image_url = await self.__download_image_from_chat(update.message, context.bot)
        text = update.message.caption
        base64_image = self.__encode_image__(image_url)

        ai_args = {"input_text": text, "input_image": base64_image, "username": update.message.from_user.first_name}

        result = self.app.ai.invoke(ai_args)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=result["output"], 
                                       connect_timeout=60)
        
    def __prepare_image_path__(self, directory, filename):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory + filename
        
    async def __download_image_from_chat(self, message, bot):
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        current_time_str = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
        filepath = self.__prepare_image_path__(self.IMAGE_FILEPATH, f"{current_time_str}_{os.path.basename(file.file_path)}")
        await file.download_to_drive(custom_path=filepath)
        return filepath

    def __encode_image__(self, image_url):
        with open(image_url, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def create(self):
        return MessageHandler(filters.PHOTO & (~filters.COMMAND), self.handle)

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

class ChangeAICommand(CommandBase):
    def __init__(self, name, app: AyanamiApp, config):
        super().__init__(name,)
        self.app = app
        self.available_ai = config

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        try:
            model = args[0].lower()
            temp = 0
            system = ''
            self.app.ai.set_ai_model(self.available_ai[model])
            print(f"args: {args}  len: {len(args)}")
            if len(args) > 1:
                temp = float(args[1])
                self.app.ai.set_ai_temp(temp)
            if len(args) > 2:
                system = args[2]
                self.app.ai.set_ai_system(system)
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=f"Updated AI with model '{self.available_ai[model]}', temp {temp} and system prompt '{system}'", 
                                       connect_timeout=60)
        except Exception as exc:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=f"Error setting AI parameters. Are your arguments correct?", 
                                       connect_timeout=60)
            raise exc

    def create(self):
        return CommandHandler(self.name, self.handle)