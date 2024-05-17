from data.db_interface import DBInterface

class TableStub(DBInterface):
    data = []

    def insert(self, entity):
        self.data.append(entity)

    def get_all(self):
        return self.data
    
    def get_with(self, criteria):
        for item in self.data:
            if(criteria(item)):
                return item
        return None

    def remove(self, entity):
        self.data.remove(entity)

    def commit(self):
        pass