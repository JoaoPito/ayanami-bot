class AuthInterface:
    def __init__(self):
        pass

    def is_authorized(self, user_id: int):
        return False
    
    def register_user(self, user_id: int, criteria):
        pass