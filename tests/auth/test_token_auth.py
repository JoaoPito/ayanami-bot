import random
import unittest

from auth.auth_interface import AuthInterface
from auth.token_auth import TokenAuth
from tests.data.stubs import TableStub

class TokenAuthTester(unittest.TestCase):

    def __get_random_user_id__(self):
        size = random.randint(5,10)
        return ''.join([str(random.randint(0,9)) for _ in range(size)])
    
    def __get_auth__(self):
        config = self.__generate_config__()
        self.table = TableStub()
        return TokenAuth(db=self.table, config=config)
    
    def __generate_config__(self):
        return {"token_size": 5, "retries": 3, "db_path": "./auth_test.db"}
    
    def __get_user_from_DB__(self, user_id):
        return self.table.get_with(lambda u: u.user_id == user_id)
    
    def __try_authorize_user_ignoring_exceptions__(self, auth, user_id, token):
        try:
            auth.try_authorize_user(user_id, token)
        except (AuthInterface.InvalidCriteriaError, AuthInterface.ForbiddenError):
            pass

    def test_if_is_not_generating_empty_tokens(self):
        auth = self.__get_auth__()
        self.assertNotEqual(auth.session_token, None, "Token is empty")

    def test_if_is_generating_tokens_with_correct_length(self):
        length = 5
        auth = self.__get_auth__()
        self.assertEqual(len(auth.session_token), length, 
                         f"Expected length of {length}, got {len(auth.session_token)}")

    def test_if_is_generating_different_tokens(self):
        auth1 = self.__get_auth__()
        auth2 = self.__get_auth__()
        self.assertNotEqual(auth1.session_token, auth2.session_token, 
                            "Auth1 token and Auth2 token should be different (most of the time)")
        
    def test_if_is_registering_new_users(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        auth.register_new_user(user_id)

        result = self.__get_user_from_DB__(user_id)
        self.assertEqual(user_id, result.user_id, f"User ID did not get registered in table")
    
    def test_if_is_not_registering_already_existing_users(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        auth.register_new_user(user_id) # Write once
        auth.register_new_user(user_id) # Write twice
        results = self.table.get_all()
        results_with_userid = list(filter(lambda u: u.user_id == user_id, results))
        self.assertEqual(len(results_with_userid), 1, f"User got registered incorrect times")

    def test_if_is_registering_new_users_after_first_try_authenticating_wrong(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        fake_token = "abcdefg"
        self.__try_authorize_user_ignoring_exceptions__(auth, user_id, fake_token)
        db_result = self.__get_user_from_DB__(user_id)
        self.assertEqual(db_result.user_id, user_id, "Could not find user registered after giving wrong token")

    def test_if_is_registering_new_users_after_first_try_authenticating_right(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        token = auth.session_token
        try:
            auth.try_authorize_user(user_id, token)
        except (AuthInterface.ForbiddenError, AuthInterface.InvalidCriteriaError):
            self.fail("Auth raised exception when shouldn't")
        db_result = self.__get_user_from_DB__(user_id)
        self.assertEqual(db_result.user_id, user_id, "Could not find user registered after giving right token")
    
    def test_if_is_decrementing_retries_after_wrong_token(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        auth.register_new_user(user_id)

        user = self.__get_user_from_DB__(user_id)
        self.assertEqual(user.retries, auth.max_retries, "Auth did not register new user with max retries")

        fake_token = "abcdefg"
        self.__try_authorize_user_ignoring_exceptions__(auth, user_id, fake_token)
        self.assertEqual(user.retries, auth.max_retries-1, "Auth did not decrement retries")
    
    def test_if_is_resetting_retries_after_right_token(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        auth.register_new_user(user_id)
        user = self.__get_user_from_DB__(user_id)
        fake_token = "abcdefg"
        real_token = auth.session_token
        self.__try_authorize_user_ignoring_exceptions__(auth, user_id, fake_token)
        auth.try_authorize_user(user_id, real_token)
        expected_retries = auth.max_retries
        self.assertEqual(user.retries, expected_retries, "Auth did not reset retries after successful login")

    def test_if_is_restricting_unauthorized_users(self):
        user_id = self.__get_random_user_id__()
        auth = self.__get_auth__()
        self.assertFalse(auth.is_authorized(user_id))

    def test_if_is_authorizing_users_after_right_token(self):
        user_id = self.__get_random_user_id__()
        auth = self.__get_auth__()
        token = auth.session_token
        auth.try_authorize_user(user_id, token)
        self.assertTrue(auth.is_authorized(user_id))

    def test_if_raises_exception_when_given_wrong_token(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        auth.register_new_user(user_id)
        fake_token = "abcdefg"
        try:
            auth.try_authorize_user(user_id, fake_token)
        except Exception as exc:
            self.assertIsInstance(exc, AuthInterface.InvalidCriteriaError, "Exception raised was not of correct type")
        else:
            self.fail("TokenAuth did not raise exception when should have")

    def test_if_blocks_user_when_runs_out_of_retries(self):
        auth = self.__get_auth__()
        user_id = self.__get_random_user_id__()
        auth.register_new_user(user_id)
        token = "abcdefg"
        for i in range(auth.max_retries):
            self.__try_authorize_user_ignoring_exceptions__(auth, user_id, token)
        try:
            auth.try_authorize_user(user_id, token)
        except Exception as exc:
            self.assertIsInstance(exc, AuthInterface.ForbiddenError, "Exception raised was not of correct type")
        else:
            self.fail("TokenAuth did not raise exception when should have")

