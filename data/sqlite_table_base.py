from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

class SQLiteTableBase(TableInterface):
    conn = None
    tablename = None
    Table = None
    Base = declarative_base()

    class EntityBase(Base):
        __tablename__ = None
        id = Column(Integer, primary_key=True)
    
    def __init__(self, db_path):
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