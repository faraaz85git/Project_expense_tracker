from fastapi import HTTPException
from starlette import status
from datetime import datetime


class NoRecordFoundException(Exception):
    def __init__(self,message="No record found with given Id."):
        self.message=message
        super().__init__(self.message)

class UserAlreadyExistsException(Exception):
    def __init__(self,message="Username already exists."):
        self.message=message
        super().__init__(self.message)

class BudgetNotSetException(Exception):
    def __init__(self,message="Budget is not set."):
        self.message=message
        super().__init__(self.message)
class UpdateException(Exception):
    def __init__(self,message="No data is provided to update"):
        self.message = message
        super().__init__(self.message)
class InvalidCategoryException(Exception):
    def __init__(self,message="No valid category is provided."
                              "It must be one of housing,transport,food,clothing,other"):
        self.message=message
        super().__init__(self.message)
class SQLiteException(Exception):
    def __init__(self,message:str="Sqlite Error."):
        self.message=message
        super().__init__(self.message)



