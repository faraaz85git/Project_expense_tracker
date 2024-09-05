import bcrypt
from db_layer.myutils import Account_manager
from db_layer.database_manager import database_manager

class Auth:
    def __init__(self):
        self.user_db=Account_manager()
        self.db_manager=database_manager()

    def login1(self,username,password):
        table_name='users'
        column=['username','password','role']
        condition=['username=?']
        data=self.db_manager.fetch_data(table_name=table_name,columns=column,where_clause=condition,parameters=[username])
        if data:
            data = data[0]
            if bcrypt.checkpw(password.encode('utf-8'),data[1]):
                return data
            else:
                return None
        else:
            return None


    def sign_up1(self,username, password,role):
        table_name='users'
        condition=['username=?']
        data=self.db_manager.fetch_data(table_name,where_clause=condition,parameters=[username])
        if data:
            return False
        else:
            column=['username','password','role']
            hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            values=[username,hashed_password,role]
            result=self.db_manager.insert_data(table_name,column,values)
            if result:
                return True
            else:
                return False
