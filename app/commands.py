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
    IMAGE_FILEPATH = "./downloaded/photos/{}"

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
        
    async def __download_image_from_chat(self, message, bot):
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        current_time_str = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
        filepath = self.IMAGE_FILEPATH.format(f"{current_time_str}_{os.path.basename(file.file_path)}")
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