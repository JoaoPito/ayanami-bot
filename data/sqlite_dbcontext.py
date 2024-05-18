from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker

from data.db_interface import DBInterface

class SQLiteDBContext(DBInterface):
    Table = None
    
    def __init__(self, table, db_path, db_base):
        self.Base = db_base
        self.Table = table
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        self.__create_table__();
        self.session = sessionmaker(bind=self.engine)()

    def __create_table__(self):
        self.Base.metadata.create_all(self.engine)

    def insert(self, entity):
        self.session.add(entity)
        self.commit()

    def get_all(self):
        return self.session.query(self.Table).all()
    
    def get_with(self, criteria):
        return self.session.query(self.Table).filter(criteria(self.Table)).first()

    def remove(self, entity):
        self.session.delete(entity)
        self.commit()

    def commit(self):
        self.session.commit()