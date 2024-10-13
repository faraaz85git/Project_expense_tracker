from fastapi import APIRouter,Path,Query,Depends,HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta,timezone
from typing import Annotated,Union
from pydantic import BaseModel,Field,field_validator
from jose import jwt,JWTError
from business_layer.Auth import Auth
from business_layer.user import User
from business_layer.Admin import Admin
from custom_exception.custom_exception import UserAlreadyExistsException,SQLiteException
from request_response_models.UserCreate import UserCreate
router=APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# class UserCreate(BaseModel):
#     user_name:str=Field(description="Username must be alpha-numeric.")
#     password:str=Field(description="Password must contain at least 10 number.")
#
#     class Config:
#         extra="forbid",
#         json_schema_extra={
#             "example":{
#                 "user_name":"AL12",
#                 "password":1234567890
#             }
#         }
#     @field_validator("user_name")
#     def validate_user_name(cls,value):
#         pass

class Token(BaseModel):
    access_token:str
    token_type:str

oauth2_bearer=OAuth2PasswordBearer(tokenUrl="auth/login")
ALGORITHM="HS256"
SECRET_KEY="197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"

def authenticate_user(user_name:str,password:str):
    auth_obj = Auth()
    data=auth_obj.login1(user_name,password)
    if data:
        return {
            "user_name":data[0],
            "password":data[1],
            "role":data[2]
        }
    else:
        return None

def get_curr_user(token:Annotated[str,Depends(oauth2_bearer)]):
   try:
       payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
       user_name=payload.get("user_name")
       role=payload.get("role")
       print("get_curr_user",payload)
       if user_name==None or role==None:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credential.Login again.")
       else:
           # return {"user_name":user_name,"role":role}
            if role=="admin":
                print(role)
                return Admin(username=user_name,password="root",role=role)
            else:
                print(role)
                return User(username=user_name, password="root", role=role)
   except HTTPException as e:
       raise
   except JWTError:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credential.Login again.")

user_dependency=Annotated[Union[User,Admin],Depends(get_curr_user)]

def create_token(user_name:str,
                 role:str,
                 expires_time:timedelta):
    try:
        encode={"user_name":user_name,"role":role}
        print("create_token",encode)
        expires=datetime.now(timezone.utc)+expires_time
        encode.update({"exp":expires})
        token=jwt.encode(encode,SECRET_KEY,ALGORITHM)
        return token
    except JWTError as e:
        raise

@router.post("/login",response_model=Token)
async def login_for_token(form_data:Annotated[OAuth2PasswordRequestForm,
                Depends()]):
    try:
        data=authenticate_user(form_data.username,
                               form_data.password)
        print("/login",data)
        if data:
            token=create_token(data["user_name"],
                               data["role"],
                               timedelta(minutes=20))
            print("/login",token)
            return {'access_token':token,'token_type':'bearer'}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Please login with valid credential.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error.")


@router.post('/sign_up',status_code=status.HTTP_204_NO_CONTENT)
async def sign_up(user:UserCreate):
    try:
        auth_obj=Auth()
        result=auth_obj.sign_up1(user.user_name,str(user.password))

    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=e.message)
    except SQLiteException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")
# @router.post("/login",status_code=status.HTTP_200_OK)
# async def login(user:user_dependency):
#     if user:
#         return {"user_name":user.get("user_name"),"status":"logged-in"}
#     else:
#         raise HTTPException(status_code=401,detail={"msg":"invalid credential."})