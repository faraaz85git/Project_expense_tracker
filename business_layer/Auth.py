import bcrypt
from db_layer.database_manager import database_manager
from custom_exception.custom_exception import UserAlreadyExistsException
class Auth:
    def __init__(self,logger):
        self.logger=logger
        self.db_manager=database_manager(logger=logger)

    def login1(self,username,password):
        try:
            self.logger.log(message="Authenticating user detail.")
            table_name='users'
            column=['username','password','role']
            condition=['username=?']
            data=self.db_manager.fetch_data(table_name=table_name,columns=column,where_clause=condition,parameters=[username])
            if data:
                data = data[0]
                if bcrypt.checkpw(password.encode('utf-8'),data[1]):
                    self.logger.log(message="Authentication success.")
                    return data
                else:
                    self.logger.log(message="Authentication failed. Password is not matched",level="warning")
                    return None
            else:
                self.logger.log(message="Authentication failed. Username not exists.",level="warning")
                return None
        except Exception as e:
            self.logger.log(message=str(e),level="error")
            raise


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
                    self.logger.log(message="User created successfully")
                    return True
                else:
                    return False

        except UserAlreadyExistsException:
            self.logger.log(message="Username already exist",level="warning")
            raise
        except Exception as e:
            self.logger.log(message=str(e),level="error")
            raise