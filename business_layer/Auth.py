import bcrypt
from db_layer.database_manager import database_manager
from custom_exception.custom_exception import UserAlreadyExistsException
class Auth:
    def __init__(self):
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


    def sign_up1(self,username, password,role="user"):
        try:
            table_name='users'
            condition=['username=?']
            data=self.db_manager.fetch_data(table_name,where_clause=condition,parameters=[username])
            if data:
                # return False
                raise UserAlreadyExistsException()
            else:
                column=['username','password','role']
                hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
                values=[username,hashed_password,role]
                result=self.db_manager.insert_data(table_name,column,values)
                if result:
                    return True
                else:
                    return False

        except UserAlreadyExistsException:
            raise
        except Exception:
            raise