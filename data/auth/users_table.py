from data.sqlite_table_base import SQLiteTableBase
from sqlalchemy import create_engine, Column, Integer, Boolean

class UsersTable(SQLiteTableBase):
    conn = None
    tablename = 'authorizedusers'

    class User(SQLiteTableBase.EntityBase):
        __tablename__ = 'authorizedusers'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, nullable=False)
        last_modified = Column(Integer, nullable=False)
        authorized_timestamp = Column(Integer, nullable=True)
        blocked = Column(Boolean, nullable=False)
        retries = Column(Integer, nullable=False)

    def __init__(self):
        self.Table = UsersTable.User
        super().__init__(self)

    def get_single(self, user_id):
        return super().get_all().filter_by(user_id=user_id).one_or_none()