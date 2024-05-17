class AuthInterface:
    def __init__(self):
        pass

    def register_new_user(self, user_id):
        pass

    def try_authorize_user(self, user_id: int, criteria):
        pass

    def is_authorized(self, user_id: int):
        return False