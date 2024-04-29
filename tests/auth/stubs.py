from auth.auth_interface import AuthInterface

class EmptyAuthStub(AuthInterface):
    is_permissive = False

    def __init__(self):
        pass

    def is_authorized(self, user_id: int):
        return self.is_permissive

class RegisteredAuthStub(AuthInterface):
    registered = {}

    def register_user(self, user_id: int):
        self.registered.append(user_id)

    def is_authorized(self, user_id: int):
        return user_id in self.registered