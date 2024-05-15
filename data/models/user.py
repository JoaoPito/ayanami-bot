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