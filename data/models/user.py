from data.sqlite_dbcontext import SQLiteDBContext
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean

Base = declarative_base()

class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, nullable=False)
        last_modified = Column(Integer, nullable=False)
        authorized = Column(Boolean, nullable=False)
        authorized_timestamp = Column(Integer, nullable=True)
        blocked = Column(Boolean, nullable=False)
        blocked_timestamp = Column(Integer, nullable=True)
        retries = Column(Integer, nullable=False)

        def __str__(self):
                return f"""\tID: {self.id}
                \tUser ID: {self.user_id}
                \tLast Modified: {self.last_modified}
                \tIs Authorized?: {self.authorized}
                \tAuthorized Timestamp: {self.authorized_timestamp}
                \tIs Blocked?: {self.blocked}
                \tBlocked Timestamp: {self.blocked_timestamp}
                \tRetries left: {self.retries}"""