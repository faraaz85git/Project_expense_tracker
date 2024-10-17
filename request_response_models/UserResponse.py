
from pydantic import BaseModel,Field


class UserResponse(BaseModel):
    user_id:int=Field(description="User id of user.")
    username:str=Field(description="Username of user.")
    role:str=Field(description="Role of a user.")


    class Config:
        json_schema_extra={
            "example":
                {
                    "user_id":1,
                    "username":"user12",
                    "role":"user"
                }
        }