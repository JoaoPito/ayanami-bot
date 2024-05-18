import os
from ai.langchain_factory import LangChainAIFactory
from app.app_builder import AyanamiAppBuilder
from app.commands.ai_commands import ChangeAICommand, ImageCommand, MessageCommand, ResetCommand
from app.commands.app_commands import PingCommand
from app.commands.auth_commands import RegisterUserCommand
import app.tools_loader as tools_loader

from auth.token_auth import TokenAuth

from chat.telegramchat_factory import TelegramChatFactory
import config

import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

config_tools = config.tools
config_ai_params = config.default_ai_params

def main():
    builder = AyanamiAppBuilder()

    chat = TelegramChatFactory().create(os.environ["TELEGRAM_BOT_TOKEN"])
    builder.set_chat(chat)

    ai_tools = tools_loader.load_tools(config_tools)
    ai = LangChainAIFactory().create(ai_tools, config_ai_params)
    builder.set_ai(ai)
    
    builder.set_authenticator(TokenAuth())
    
    app = builder.build_app()

    # AI commands
    app.add_command(MessageCommand(app))
    app.add_command(ImageCommand(app))
    app.add_command(ResetCommand('reset', app))
    app.add_command(ChangeAICommand('switch_ai', app, config.available_ai))

    # App commands
    app.add_command(PingCommand('ping', app))

    # Auth commands
    app.add_command(RegisterUserCommand('auth', app))

    app.run()

if __name__ == "__main__":
    main()
