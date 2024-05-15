from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker

from data.table_interface import TableInterface

class SQLiteTableBase(TableInterface):
    Table = None
    
    def __init__(self, table, db_path, db_base):
        self.Base = db_base
        self.Table = table
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=True)
        self.__create_table__();
        self.session = sessionmaker(bind=self.engine)()

    def __create_table__(self):
        self.Base.metadata.create_all(self.engine)

    def insert(self, entity):
        self.session.add(entity)
        self.commit()

    def get_all(self):
        return self.session.query(self.Table)

    def remove(self, entity):
        self.session.delete(entity)
        self.commit()

    def commit(self):
        self.session.commit()