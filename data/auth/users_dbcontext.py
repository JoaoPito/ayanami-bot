from data.sqlite_table_base import SQLiteTableBase

class UsersDBContext(SQLiteTableBase):
    def get_by_user_id(self, user_id):
        return super().get_all().filter_by(user_id=user_id).one_or_none()
