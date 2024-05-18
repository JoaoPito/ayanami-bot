class AuthInterface:
    def __init__(self):
        pass

    def register_new_user(self, user_id):
        pass

    def try_authorize_user(self, user_id: int, criteria):
        pass

    def is_authorized(self, user_id: int):
        return False
    
    class ForbiddenError(Exception):
        "Raised when User cannot have access to resource"
        pass

    class InvalidCriteriaError(Exception):
        "Raised when given unexpected criteria for access"
        pass