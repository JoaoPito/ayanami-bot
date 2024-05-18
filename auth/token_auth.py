from datetime import datetime
import random
import string
from uuid import uuid4
from auth.auth_interface import AuthInterface
from data.db_interface import DBInterface
from data.models.user import User

from sqlalchemy.orm.exc import MultipleResultsFound

UNREGISTERED_USER_ERROR_MSG = "User is not registered"
BLOCKED_USER_ERROR_MSG = "User with ID {user_id} is blocked"
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

    def __get_user_by_id__(self, user_id):
        return self.db.get_with(lambda u: u.user_id == user_id)
        
    def __is_user_blocked__(self, user_id):
        user = self.__get_user_by_id__(user_id)
        return user.blocked

    def __is_token_correct__(self, token):
        return token == self.session_token
    
    def __get_retries_for_user__(self, user_id):
        user = self.db.get_with(lambda u: u.user_id == user_id)
        return user.retries
    
    def __decrement_user_retries__(self, user_id):
        timestamp = datetime.now().isoformat()
        user = self.db.get_with(lambda u: u.user_id == user_id)
        user.retries = user.retries - 1
        user.last_modified = timestamp
        self.db.commit()
    
    def __block_user__(self, user_id):
        timestamp = datetime.now().isoformat()
        user = self.db.get_with(lambda u: u.user_id == user_id)
        user.retries = 0
        user.authorized = False
        user.blocked = True
        user.last_modified = timestamp
        user.blocked_timestamp = timestamp
        self.db.commit()
    
    def __authorize_user__(self, user_id):
        timestamp = datetime.now().isoformat()
        user = self.db.get_with(lambda u: u.user_id == user_id)
        user.retries = self.max_retries
        user.blocked = False
        user.authorized = True
        user.last_modified = timestamp
        user.authorized_timestamp = timestamp
        self.db.commit()

    def __block_user_if_run_out_of_retries__(self, user_id):
        retries_left = self.__get_retries_for_user__(user_id)
        if retries_left <= 0:
            self.__block_user__(user_id)

    def register_new_user(self, user_id):
        if(not self.db.get_with(lambda u: u.user_id == user_id)):
            self.__create_new_user__(user_id=user_id)

    def try_authorize_user(self, user_id: int, criteria):
        self.register_new_user(user_id)
        if(self.__is_user_blocked__(user_id)):
            raise AuthInterface.ForbiddenError(BLOCKED_USER_ERROR_MSG.format(user_id=user_id))
        if(not self.__is_token_correct__(criteria)):
            self.__decrement_user_retries__(user_id)
            self.__block_user_if_run_out_of_retries__(user_id)
            raise AuthInterface.InvalidCriteriaError(INVALID_TOKEN_ERROR)
        self.__authorize_user__(user_id)

    def is_authorized(self, user_id: int):
        user = self.__get_user_by_id__(user_id)
        if(user == None):
            return False
        return user.authorized