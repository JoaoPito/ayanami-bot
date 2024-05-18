from data.models.user import User, Base
from data.sqlite_dbcontext import SQLiteDBContext

def create_dbcontext(path="./app.db"):
    return SQLiteDBContext(User, path, Base)