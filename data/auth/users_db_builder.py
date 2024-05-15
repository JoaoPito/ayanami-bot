from data.auth.users_dbcontext import UsersDBContext
from data.models.user import User, Base

def create_table():
    return UsersDBContext(User, Base)