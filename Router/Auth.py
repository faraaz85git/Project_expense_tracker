from fastapi import APIRouter,Path,Query,Depends,Request,HTTPException
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

def authenticate_user(user_name:str,password:str,logger):
    try:
        auth_obj = Auth(logger=logger)
        data=auth_obj.login1(user_name,password)
        if data:
            return {
                "user_name":data[0],
                "password":data[1],
                "role":data[2]
            }
        else:
            return None
    except Exception as e:
        logger.log(message=f"Authentication failed.{str(e)},",level="error")
        raise

def get_curr_user(token:Annotated[str,Depends(oauth2_bearer)],request:Request):
   try:
       logger = request.state.logger
       logger.log(message="Token validation starts.")
       payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
       user_name=payload.get("user_name")
       role=payload.get("role")

       # print("get_curr_user",payload)
       if user_name==None or role==None:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credential.Login again.")
       else:
           # return {"user_name":user_name,"role":role}
            if role=="admin":
                logger.log(message="Token validation success.")
                return Admin(username=user_name,role=role,logger=logger)
            else:
                logger.log(message="Token validation success.")
                return User(username=user_name, role=role,logger=logger)
   except HTTPException as e:
       request.state.logger.log(message=f"Token validation failed. {e.detail}",level="error")
       raise
   except JWTError as e:
       request.state.logger.log(message=f"Token validation failed. {str(e)}",level="error")
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credential.Login again.")
   except Exception as e:
       request.state.logger.log(message=f"Token validation failed. {str(e)}",level="error")
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credential.Login again.")


user_dependency=Annotated[Union[User,Admin],Depends(get_curr_user)]

def create_token(user_name:str,
                 role:str,
                 expires_time:timedelta,
                 logger):
    try:
        encode={"user_name":user_name,"role":role}
        print("create_token",encode)
        expires=datetime.now(timezone.utc)+expires_time
        encode.update({"exp":expires})
        token=jwt.encode(encode,SECRET_KEY,ALGORITHM)
        logger.log(message="Token generated successfully.")
        return token
    except JWTError as e:
        logger.log(message=f"Token generation failed.{str(e)}",level="error")
        raise

@router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login_for_token(form_data:Annotated[OAuth2PasswordRequestForm,
                Depends()],request:Request):
    try:
        data=authenticate_user(form_data.username,
                               form_data.password,
                               request.state.logger)
        print("/login",data)
        if data:
            token=create_token(data["user_name"],
                               data["role"],
                               timedelta(minutes=20),logger=request.state.logger)
            print("/login",token)
            return {'access_token':token,'token_type':'bearer'}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Please login with valid credential.")
    except HTTPException as e:
        request.state.logger.log(message=f"{e.status_code} {e.detail}",level="error")
        raise
    except Exception as e:
        request.state.lgger.log(message=str(e),level="error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@router.post('/sign_up',status_code=status.HTTP_200_OK)
async def sign_up(user:UserCreate,request:Request):
    try:
        request.state.logger.log(message="Request is processing")
        auth_obj=Auth(request.state.logger)
        result=auth_obj.sign_up1(user.user_name,str(user.password))
        return {"status":"created"}
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=e.message)
    except SQLiteException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")
    except Exception as e:
        request.state.logger.log(message=str(e),level="error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error.")
# @router.post("/login",status_code=status.HTTP_200_OK)
# async def login(user:user_dependency):
#     if user:
#         return {"user_name":user.get("user_name"),"status":"logged-in"}
#     else:
#         raise HTTPException(status_code=401,detail={"msg":"invalid credential."})