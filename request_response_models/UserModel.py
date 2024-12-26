from pydantic import BaseModel, Field, field_validator


class UserModel(BaseModel):
    username:str=Field()
    password:str=Field()

