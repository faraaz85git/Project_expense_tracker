from pydantic import BaseModel,Field,field_validator
from db_layer.myutils import validate_username,validate_password


class UserCreate(BaseModel):
    user_name:str=Field(min_length=2,description="Username must be alpha-numeric.")
    password:int=Field(description="Password should contain at least 10 numbers.")

    class Config:
        json_schema_extra={
            "example":{
                "user_name":"user1234",
                "password":12345678910
            }
        }
    @field_validator("user_name")
    def validate_user_name(cls,value):
        if not validate_username(value):
            raise ValueError("Invalid username.Username must be alpha-numeric.")
        else:
            return value

    @field_validator("password")
    def validate_pass_word(cls,value) :
        if validate_password(str(value)) and type(value)==int:
            return value
        else:
            raise ValueError("Invalid password.Password must contain at least 10 numbers")
