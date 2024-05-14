from uuid import uuid4
from auth.auth_interface import AuthInterface

class TokenAuth(AuthInterface):
    def __init__(self):
        pass

    def __generate_token__(self):
        pass

    def is_authorized(self, user_id: int):
        return False
    
    def register_user(self, user_id: int, token: uuid4):
        raise AttributeError("User is blocked")