from data.sqlite_table_base import SQLiteTableBase
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean

Base = declarative_base()

class User(SQLiteTableBase.EntityBase):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, nullable=False)
        last_modified = Column(Integer, nullable=False)
        authorized_timestamp = Column(Integer, nullable=True)
        blocked = Column(Boolean, nullable=False)
        retries = Column(Integer, nullable=False)