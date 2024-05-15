from data.models.user import User, Base
from data.sqlite_dbcontext import SQLiteDBContext

def create_table():
    return SQLiteDBContext(User, Base)