from ai.ai_interface import AIInterface
from app.app import AyanamiApp
from auth.auth_interface import AuthInterface
from chat.chatbase import ChatBase

error_not_assigned_message = "Parameter '{param}' needed for App wasn't set."
param_names = {"AI": "AI", "Chat": "Chat"}

class AyanamiAppBuilder():
    tools = []
    ai: AIInterface|None = None
    chat: ChatBase|None = None
    auth: AuthInterface|None = None

    def __init__(self):
        pass

    def __check_assigned_params__(self): 
        if not self.ai:
            raise TypeError(error_not_assigned_message.format(param=param_names['AI']))
        if not self.chat:
            raise TypeError(error_not_assigned_message.format(param=param_names['Chat']))

    def build_app(self) -> AyanamiApp:
        self.__check_assigned_params__()
        return AyanamiApp(self.ai, self.chat, self.auth) 

    def set_ai(self, ai:AIInterface):
        self.ai = ai

    def set_chat(self, chat:ChatBase):
        self.chat = chat

    def set_authenticator(self, auth:AuthInterface):
        self.auth = auth
