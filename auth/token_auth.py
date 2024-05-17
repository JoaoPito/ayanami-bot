from datetime import datetime
import random
import string
from uuid import uuid4
from auth.auth_interface import AuthInterface
from data.db_interface import DBInterface
from data.models.user import User

from sqlalchemy.orm.exc import MultipleResultsFound

UNREGISTERED_USER_ERROR_MSG = "User is not registered"
BLOCKED_USER_ERROR_MSG = "User is blocked"
INVALID_TOKEN_ERROR = "Token is invalid"

REGISTERED_USERS_TABLE = "auth_users"

class TokenAuth(AuthInterface):
    session_token = None

    def __init__(self, db:DBInterface, config):
        self.token_length = config["token_size"]
        self.max_retries = config['retries']
        self.db = db
        self.session_token = self.__generate_token__(self.token_length)

    def __generate_token__(self, length):
        characters = string.ascii_letters + string.digits
        token = ''.join(random.choice(characters) for _ in range(length))
        return token

    def __create_new_user__(self, user_id):
        timestamp = datetime.now().isoformat()
        new_user = User(user_id=user_id, 
                        last_modified=timestamp,
                        authorized=False,
                        authorized_timestamp=0, 
                        blocked=False,
                        blocked_timestamp=0, 
                        retries=self.max_retries)
        self.db.insert(new_user)

    def __except_if_user_is_blocked__(self, user_id):
        user = self.db.get_with(lambda u: u.user_id == user_id)
        if user == None:
            self.__create_new_user__(user_id)
            return
        if user.blocked:
            raise AssertionError(BLOCKED_USER_ERROR_MSG)

    def __is_token_correct__(self, token):
        return token == self.session_token

    def __user_entered_invalid_token__(self, user_id):
        retries_left = self.__get_retries_for_user__(user_id)
        if retries_left <= 0:
            self.__block_user__(user_id)
        else:
            self.__decrement_user_retries__(user_id)
        raise AssertionError(INVALID_TOKEN_ERROR)

    def register_new_user(self, user_id):
        if(not self.db.get_with(lambda u: u.user_id == user_id)):
            self.__create_new_user__(user_id=user_id)

    def try_authorize_user(self, user_id: int, criteria):
        # Verify if is registered
        # If user is blocked raise Exception
        # If given token is wrong dec retries & raise Exception
        # else authorize user
            # clear retries and blocked flag and timestamps
        raise NotImplementedError()

    def is_authorized(self, user_id: int):
        # Fetch DB for user
        # If is null return False
        # else return user.authorized and not user.blocked
        raise NotImplementedError()