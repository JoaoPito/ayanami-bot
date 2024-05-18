import os
from ai.langchain_factory import LangChainAIFactory
from app.app_builder import AyanamiAppBuilder
from app.commands.ai_commands import ChangeAICommand, ImageCommand, MessageCommand, ResetCommand
from app.commands.app_commands import PingCommand, StartCommand
from app.commands.auth_commands import RegisterUserCommand, TryAuthenticateUserCommand
import app.tools_loader as tools_loader

from auth.token_auth import TokenAuth

from chat.telegramchat_factory import TelegramChatFactory
import config

import logging

from data.users_db_builder import create_dbcontext

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

config_tools = config.tools
config_ai_params = config.default_ai_params
config_auth = config.auth_config

def main():
    builder = AyanamiAppBuilder()

    chat = TelegramChatFactory().create(os.environ["TELEGRAM_BOT_TOKEN"])
    builder.set_chat(chat)

    ai_tools = tools_loader.load_tools(config_tools)
    ai = LangChainAIFactory().create(ai_tools, config_ai_params)
    builder.set_ai(ai)
    
    auth = TokenAuth(create_dbcontext(path="./users.db"), config_auth)
    builder.set_authenticator(auth)
    
    app = builder.build_app()

    # AI commands
    app.add_command(MessageCommand(app))
    app.add_command(ImageCommand(app))
    app.add_command(ResetCommand('reset', app))
    app.add_command(ChangeAICommand('switch_ai', app, config.available_ai))

    # App commands
    app.add_command(PingCommand('ping', app))

    # Auth commands
    app.add_command(StartCommand('start', app))
    app.add_command(TryAuthenticateUserCommand('auth', app))

    print(f"> IMPORTANT: This session token is: '{auth.session_token}', use it to authenticate with '/auth TOKEN.'")

    app.run()

if __name__ == "__main__":
    main()
